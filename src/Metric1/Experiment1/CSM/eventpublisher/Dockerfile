FROM eclipse-temurin:25-jre

WORKDIR /publisher

COPY CSMSmartFactoryEventPublisher.jar CSMSmartFactoryEventPublisher.jar
COPY zenohSrv.json5 ./zenoh/zenohSrv.json5

CMD ["java", "-jar", "CSMSmartFactoryEventPublisher.jar"]