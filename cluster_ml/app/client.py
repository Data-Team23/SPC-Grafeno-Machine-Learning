import pandas as pd
from sklearn.preprocessing import scale, PowerTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score


class RFMClient:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.df = None
        self.df_rfm = None
        self.cluster_metrics_results = []

    def load_data(self):
        self.df = pd.read_csv(self.csv_path, encoding='latin1')
        self.df = self.df[self.df['deleted_at'].isnull()]
        self.df['created_at'] = pd.to_datetime(self.df['created_at'])
        self.df = self.df.query('value < 100000 & value > 0')

    def calculate_rfm(self):
        self.load_data()
        self.df_rfm = (
            self.df.groupby('participant_id')
            .agg(
                R=('created_at', lambda x: (pd.Timestamp.today() - x.max()).days),
                F=('asset_id', 'nunique'),
                M=('value', 'mean'),
            )
        )
        return self.df_rfm.reset_index().to_dict(orient='records')

    def preprocess_rfm(self):
        self.df_rfm = self.df_rfm.query('F < 100000 & M < 20000')
        scaler = PowerTransformer()
        self.df_rfm = pd.DataFrame(
            scaler.fit_transform(self.df_rfm), 
            index=self.df_rfm.index, 
            columns=self.df_rfm.columns
        )
        self.df_rfm = self.df_rfm.apply(lambda x: x.clip(upper=x.quantile(0.95)))
        return self.df_rfm.reset_index().to_dict(orient='records')

    def cluster_rfm(self, n_clusters=4):
        X = self.df_rfm.copy()
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        self.df_rfm['Cluster'] = kmeans.fit_predict(X)
        return self.df_rfm.reset_index().to_dict(orient='records')

    def get_cluster_centers(self):
        """Retorna os centros dos clusters ajustados com as colunas apropriadas."""
        kmeans = KMeans(n_clusters=4, random_state=0)
        X = self.df_rfm.drop(columns=['Cluster'], errors='ignore')
        kmeans.fit(X)
        centers = pd.DataFrame(kmeans.cluster_centers_, columns=X.columns)
        centers.index = [f"Cluster {i+1}" for i in range(len(centers))]
        return centers.reset_index().to_dict(orient='records')

    def evaluate_clusters(self):
        X = self.df_rfm.drop(columns=['Cluster'], errors='ignore')
        for k in range(2, 11):
            model = KMeans(n_clusters=k, random_state=0)
            labels = model.fit_predict(X)
            cluster_results = {
                'k': k,
                'inertia': model.inertia_,
                'silhouette_score': silhouette_score(X, labels),
                'davies_bouldin_score': davies_bouldin_score(X, labels),
                'calinski_harabasz_score': calinski_harabasz_score(X, labels),
            }
            self.cluster_metrics_results.append(cluster_results)
        return self.cluster_metrics_results
