from rest_framework.views import APIView
from rest_framework.response import Response
from .client import RFMClient
from .models import CSVFile
from .forms import CSVUploadForm
from django.shortcuts import render, redirect


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('analyze_csv')
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})


def get_csv_processor():
    csv_file = CSVFile.objects.last()
    if not csv_file:
        return None
    return csv_file.file.path


class RFMDataView(APIView):
    def get(self, request):
        csv_path = get_csv_processor()
        if not csv_path:
            return Response({"error": "No CSV file found."}, status=404)
        
        client = RFMClient(csv_path)
        data = client.calculate_rfm()
        return Response(data)


class PreprocessedRFMView(APIView):
    def get(self, request):
        csv_path = get_csv_processor()
        if not csv_path:
            return Response({"error": "No CSV file found."}, status=404)
        
        client = RFMClient(csv_path)
        client.calculate_rfm()
        data = client.preprocess_rfm()
        return Response(data)

class ClusteredDataView(APIView):
    def get(self, request):
        csv_path = get_csv_processor()
        if not csv_path:
            return Response({"error": "No CSV file found."}, status=404)
        
        client = RFMClient(csv_path)
        client.calculate_rfm()
        client.preprocess_rfm()
        data = client.cluster_rfm()
        return Response(data)

class ClusterCentersView(APIView):
    def get(self, request):
        csv_path = get_csv_processor()
        if not csv_path:
            return Response({"error": "No CSV file found."}, status=404)
        
        client = RFMClient(csv_path)
        client.calculate_rfm()
        client.preprocess_rfm()
        data = client.get_cluster_centers()
        return Response(data)

class ClusterMetricsView(APIView):
    def get(self, request):
        csv_path = get_csv_processor()
        if not csv_path:
            return Response({"error": "No CSV file found."}, status=404)
        
        client = RFMClient(csv_path)
        client.calculate_rfm()
        client.preprocess_rfm()
        data = client.evaluate_clusters()
        return Response(data)
