import os
import subprocess
import tempfile
import uuid
from pathlib import Path
from flask import Flask, request, render_template, send_file, jsonify

app = Flask(__name__)
UPLOAD_DIR = Path("/tmp/vtracer-output")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    if "image" not in request.files:
        return jsonify({"error": "Nenhuma imagem enviada"}), 400
    
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "Arquivo vazio"}), 400
    
    # Parâmetros opcionais
    colormode = request.form.get("colormode", "color")
    mode = request.form.get("mode", "spline")
    filter_speckle = request.form.get("filter_speckle", "4")
    color_precision = request.form.get("color_precision", "6")
    gradient_step = request.form.get("gradient_step", "16")
    corner_threshold = request.form.get("corner_threshold", "60")
    path_precision = request.form.get("path_precision", "4")
    
    ext = Path(file.filename).suffix.lower()
    job_id = str(uuid.uuid4())[:8]
    
    input_path = UPLOAD_DIR / f"{job_id}_input{ext}"
    output_path = UPLOAD_DIR / f"{job_id}_output.svg"
    
    file.save(str(input_path))
    
    cmd = [
        "/usr/local/bin/vtracer",
        "--input", str(input_path),
        "--output", str(output_path),
        "--colormode", colormode,
        "--mode", mode,
        "--filter_speckle", filter_speckle,
        "--color_precision", color_precision,
        "--gradient_step", gradient_step,
        "--corner_threshold", corner_threshold,
        "--path_precision", path_precision,
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if not output_path.exists():
            return jsonify({
                "error": "Falha na conversão",
                "stderr": result.stderr,
                "stdout": result.stdout
            }), 500
        
        # Ler resultado
        svg_content = output_path.read_text()
        svg_size = output_path.stat().st_size
        
        # Limpar
        input_path.unlink(missing_ok=True)
        output_path.unlink(missing_ok=True)
        
        return jsonify({
            "success": True,
            "svg": svg_content,
            "size_bytes": svg_size,
            "stats": {
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        })
    
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout (60s) — imagem muito grande?"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
