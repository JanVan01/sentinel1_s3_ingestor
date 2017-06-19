# Sentinel1 S3 Ingestor

Downloads Sentinel1 sata and stores them to a AWS S3 Bucket

## Installation
```
git clone https://github.com/JanVan01/sentinel1_s3_ingestor.git
cd sentinel1_s3_ingestor
pip install -r requirements.txt
```

Modify `credentials.py.sample` file and fill in 
- your scihub credentials you can get from here: https://scihub.copernicus.eu/dhus/#/home
- your AWS credentials
- your AWS S3 bucket you want to upload your data

Change `extend.geojson` to your desired bounding box

Change the start date in `/api/copernicus.py`

You are now ready to go!

## Run
run `python ingestor.py`
