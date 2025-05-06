from flask import Flask, send_from_directory, jsonify, render_template
from flask_cors import CORS
import os
from config import Config
from routes.enhance_routes import enhance_bp
from routes.filter_routes import filter_bp
from routes.adjust_routes import adjust_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS (for frontend integration, if needed)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(enhance_bp, url_prefix='/enhance')
    app.register_blueprint(filter_bp, url_prefix='/filter')
    app.register_blueprint(adjust_bp, url_prefix='/adjust')

    # Index route for the web app
    @app.route('/')
    def index():
        return render_template('index.html')
    
    #Basic health check route
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy', 'message': 'Flask API is running'})

    # Serve uploaded files (images)
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    @app.route('/filtered_images/<filename>')
    def filtered_file(filename):
        return send_from_directory(Config.FILTERED_FOLDER, filename)

    @app.route('/adjusted/<filename>')
    def adjusted_file(filename):
        return send_from_directory(Config.ADJUSTED_FOLDER, filename)

    # Error Handlers
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()

    # Ensure upload directories exist
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(Config.FILTERED_FOLDER, exist_ok=True)
    os.makedirs(Config.ADJUSTED_FOLDER, exist_ok=True)

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)  # Set debug=True to see detailed errors how can divide this code in different files


