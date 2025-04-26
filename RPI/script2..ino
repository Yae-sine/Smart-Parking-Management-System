#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Identifiants Wi-Fi
const char* ssid = "jawad";
const char* password = "01020304";

// Adresse du serveur Flask
const char* server = "http://192.168.14.51:5000/spots";

// Broches assignées
const int ledRouge = 12;  // D12 : LED rouge (parking plein)
const int ledVerte = 13;  // D13 : LED verte (au moins une place libre)

void setup() {
  Serial.begin(115200);

  pinMode(ledRouge, OUTPUT);
  pinMode(ledVerte, OUTPUT);

  digitalWrite(ledRouge, LOW);
  digitalWrite(ledVerte, LOW);

  Serial.print("🔗 Connexion au Wi-Fi : ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(1000);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ Wi-Fi connecté !");
    Serial.print("📡 IP locale : ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ Connexion Wi-Fi échouée !");
  }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(server);
    int httpCode = http.GET();

    if (httpCode == 200) {
      String payload = http.getString();
      StaticJsonDocument<512> doc;
      DeserializationError error = deserializeJson(doc, payload);

      if (!error) {
        int libres = 0;

        for (int i = 0; i < 4; i++) {
          String key = "spot" + String(i + 1);
          String status = doc[key];
          if (status == "available") {  
            libres++;
          }
        }

        if (libres > 0) {
          digitalWrite(ledVerte, HIGH);  // allume la verte
          digitalWrite(ledRouge, LOW);   // éteint la rouge
          Serial.println("🟢 Des places sont disponibles.");
        } else {
          digitalWrite(ledVerte, LOW);   // éteint la verte
          digitalWrite(ledRouge, HIGH);  // allume la rouge
          Serial.println("🔴 Parking complet !");
        }

      } else {
        Serial.println("❌ Erreur de parsing JSON");
      }

    } else {
      Serial.print("❌ Erreur HTTP : ");
      Serial.println(httpCode);
    }

    http.end();

  } else {
    Serial.println("🔁 Wi-Fi perdu, reconnexion...");
    WiFi.begin(ssid, password);
  }

  delay(3000);
}