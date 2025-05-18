from flask import Flask, render_template, request, redirect, url_for
import boto3
import os

app = Flask(__name__)
s3 = boto3.client('s3', region_name='ap-southeast-1')  # use your region
BUCKET_NAME = 'tranthanhdaibucket'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                s3.upload_fileobj(file, BUCKET_NAME, file.filename)
            except Exception as e:
                return f"Upload failed: {str(e)}"
        return redirect(url_for('index'))

    # List files in the bucket
    try:
        objects = s3.list_objects_v2(Bucket=BUCKET_NAME)
        files = [obj['Key'] for obj in objects.get('Contents', [])]
    except Exception as e:
        files = []
    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    try:
        s3.download_file(BUCKET_NAME, filename, filename)
        return f"Downloaded: {filename}"
    except Exception as e:
        return f"Download failed: {str(e)}"

@app.route('/delete/<filename>')
def delete_file(filename):
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
        return redirect(url_for('index'))
    except Exception as e:
        return f"Delete failed: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
