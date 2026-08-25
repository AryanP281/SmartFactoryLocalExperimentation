FROM eclipse-temurin:25-jre

WORKDIR /collector
COPY CSMMetricsCollector.jar CSMMetricsCollector.jar
COPY zenoh.json5 ./zenoh/zenoh.json5

CMD ["java", "-jar", "CSMMetricsCollector.jar"]