from flask import Flask, request, render_template
from pathlib import Path

from youtube.loggers import logger
from youtube.pipeline import PredictionPipeline, CustomData

app = Flask(__name__)

try:
    model_path = Path("artifacts/model_trainer/model.pkl")
    preprocessor_path = Path("artifacts/data_transformation/preprocessor.pkl")
    prediction_pipeline = PredictionPipeline(model_path, preprocessor_path)
    logger.info(f"Prediction Pipeline Initialized Successfully")
except Exception as e:
    logger.info(f"Failed to Initialize Prediction Pipeline: {e}")
    prediction_pipeline = None

@app.route('/')
def index():
    """Render The Home with the Prediction Form"""
    return render_template("index.html")

@app.route("/predictdata", methods = ['GET', 'POST'])
def predict_datapoint():
    """Handle Prediction Requests"""
    if request.method == 'GET':
        return render_template('home.html')
    
    try:
        data = CustomData(
            video_duration=float(request.form.get('video_duration')),
            days_since_publish=int(request.form.get('days_since_publish')),
            day=int(request.form.get('day')),
            month=int(request.form.get('month')),
            year=int(request.form.get('year')),
            revenue_per_1000_views=float(request.form.get('revenue_per_1000_views')),
            monetized_playbacks=float(request.form.get('monetized_playbacks')),
            views=float(request.form.get('views')),
            watch_time_hours=float(request.form.get('watch_time_hours')),
            subscribers=float(request.form.get('subscribers')),
            impressions=float(request.form.get('impressions')),
            video_thumbnail_ctr=float(request.form.get('video_thumbnail_ctr')),
            average_view_percentage=float(request.form.get('average_view_percentage')),
            average_view_duration=float(request.form.get('average_view_duration')),
            day_of_week=int(request.form.get('day_of_week'))
        )

        pred_df = data.get_data_as_data_frame()
        logger.info(f"Created Prediction Dataframe: {pred_df.head()}")

        if prediction_pipeline is None:
            raise Exception("Prediction Pipeline not Initialized")
        
        results = prediction_pipeline.predict(pred_df)
        logger.info(f"Prediction Results: {results}")

        prediction_result = round(results[0], 2)

        return render_template('home.html', results=prediction_result)
    
    except Exception as e:
        logger.error(f"Error During Prediction: {e}")
        error_message = f"An Error occured during prediction: {str(e)}"
        return render_template('home.html', error= error_message)

@app.route('health')
def health_check():
    """Health Check Endpoint"""
    return {"status": "healthy", "model_loaded": prediction_pipeline is not None}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
    