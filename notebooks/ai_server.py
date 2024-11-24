from flask import Flask, jsonify
from kmeans import df_rfm_clip_scaled  # Importando o resultado da IA 

app = Flask(__name__)

@app.route('/api/clustering', methods=['GET'])
def get_clustering_results():
    try:
        results = df_rfm_clip_scaled.copy()
        results['participant_id'] = df_rfm_clip_scaled.index
        return jsonify(results.to_dict(orient='records'))  # Retorna os dados como JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # O servidor roda na porta 5000