#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "";
const char* password = "";
const char* serverName = "http://192.168.1.6:8080/process";

const char* placeholder_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAclBMVEUAAAD///8UFBTR0dGnp6eRkZHl5eW6urri4uL6+vrY2NhZWVm3t7exsbH19fV1dXU8PDxmZmbs7OzNzc0pKSmXl5cfHx9ra2vExMRUVFSAgICEhIScnJw9PT0zMzPv7+8ZGRlgYGBMTEwVFRWKioolJSXGlSmvAAAEuklEQVR4nO2Z6YKaMBhFE0UFZFHcwGWcmU7f/xXLkoSw1KlInd7pPX+UkGAOSb4siv3ke7MXE/G9mdAQHhriQ0N8aIgPDfGhIT40xIeG+NAQHxriQ0N8aIgPDfGhIT40xIeG+NAQHxriQ0N8aIgPDfGhIT40xIeG+NAQHxriQ0N8aIgPDfGhIT40xIeG+NAQHxriQ0N8aIgPDfGhIT40xIeG+NAQHxriQ0N8aIgPDfGhIT40xIeG+HyJ4eVwPMbL/e08x3MYOrN1I/HneRG+3fljww0P6cImPK9b9xO3Yt5Mj6dS4aUHlbaYlxl3Os8q8HQm6Z9MUUc6x9k8ua/Gww13skNo39+Y5KOVml0bJZKsTFXSjsqUNh/rqRcR+uXHyburnsMNZ11DGVkPq1OndeKpU+TUMVx5nUxBmS5FKD3pi7DxJp9rKN1eF5O47imybhmu+p6b5jfCswjzT5mJuxpxZENp4oBvJX7oxG7r5H2wZdiXR8pZnmktQvd0zt/Xcw29aY5vRpfuQBO7er5KPKrr6TJvKjOOjw3DhSkVbVLrNeWjMxZh4hTZ5W+q9HcMVaR8UxVJm3eD6uO1SlQRRI3LfV2kNtyapq3Cy1lfO+IjFcEmf0sia0Xn5xjmQaBh6JZXibLY2Ymm09ZPqA1DLfhDZdJDN8qb7n2Vh97DNmrNS08y/Kg7mjBN4YjIzuQ22lBcXL9gYxtGSmhpfkd1A/kiLmXgXV0dcQ+jGTrV5aq6Up0r023yUqbqud6NW88yhi8qh1/f07E1H3/7qUy8a7vwJ4xleGl20qTqakIs7aZ1pCFKd3Uz1YaxbHbkgm3Fa3Vxdz0fNozCIAgWvhksJcp3IfTEf62qJ5vMnUvLUAeWy8BK9TDqfGgWL6pvFuFQxc/3Mt3pFPHL/msMdaB52KtmVMPgp7oX1fVU/U7Nk2m3UGNN868bSllFgay62JQX1Xfdf4/dJcsLlGHZMXWAr3TVHsPElTiNmkX8nnG4etxM87ChWmsvXevtq3Y67wpUx1xYRV9jx162Tm7H0gcZbT7UWnH/DqJQ376VVEHHWpgebs6HOunYrsDTDVNdy75wUnoo86suoRemp5trGj00h04g4xmqWob23tcmNa1hZu1Et07PulRXa6kTBlZzPEO9uNqZsdTGqJttsmmv3+8tTFe+a18/qmFyiHNOen2cL0XrA5omsdn7zcvTmffEqP/B/vD2ydzfNGwRmZaJs2VFpio9tQ4oPNc1E2PwJ3v881DB0Q3X+oDGGjeZaavuqq17itF7TrMZLDi24cwc0ARWVtUsH71h9iI+P2tLe2vwBYbXt3w2V9/tfbjqpkWEaZ+yuuX4+uS8dOhU+KBhq66eG5TnbKdkXpDYWddV2rX4qYljLdo26j0sygxJ75m3++D65iv+t9jGOycMz6fsVqbe/y2GwP+e8KEhPjTEh4b40BAfGuJDQ3xoiA8N8aEhPjTEh4b40BAfGuJDQ3xoiA8N8aEhPjTEh4b40BAfGuJDQ3xoiA8N8aEhPjTEh4b40BAfGuJDQ3xoiA8N8aEhPjTEh4b40BAfGuJDQ3xoiA8N8aEhPjTEh4b40BAfGuJDQ3xoiM//YLiffG/2vwBe6TAMGzeAXgAAAABJRU5ErkJggg==";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    String postData = "{\"image\":\"" + String(placeholder_image_base64) + "\"}";

    http.begin(serverName);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.print("Response: ");
      Serial.println(response);
    } else {
      Serial.print("Error on HTTP request: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi not connected");
  }

  delay(1000);
}