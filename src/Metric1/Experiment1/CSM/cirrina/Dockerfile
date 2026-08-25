FROM eclipse-temurin:25-jre

WORKDIR /opt/cirrina

COPY lib/ /opt/cirrina/lib/

ENTRYPOINT ["java","--enable-native-access=ALL-UNNAMED","--sun-misc-unsafe-memory-access=allow","-cp","/opt/cirrina/lib/*","at.ac.uibk.dps.cirrina.CirrinaKt"]