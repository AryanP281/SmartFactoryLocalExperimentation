FROM eclipse-temurin:25-jre

WORKDIR /collector

COPY DaprMetricsCollector.jar Collector.jar

ENTRYPOINT ["java", "-jar", "Collector.jar"]