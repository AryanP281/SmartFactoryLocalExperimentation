FROM eclipse-temurin:25-jre

WORKDIR /service

COPY backend.jar backend.jar
COPY yolov8n.onnx ./models/yolov8n.onnx
ADD imgs ./imgs

CMD ["java", "-jar", "backend.jar"]