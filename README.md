# ActiveMQ 

---

## Setup
- Inštalácia Apache ActiveMQ
    - Systém Apache ActiveMQ je z velkej časti v Jave (okrem knižnice wrapper) a vyžaduje, aby na systéme bola nainštalovaná Java 8.
    - Stiahnutie a rozbalenie Apache ActiveMQ bud priamo zo [stránky](https://activemq.apache.org/components/classic/download/) na základe verzie OS alebo pomocou príkazu pre sťiahnutie tar.
    - ```$ wget -O apache-activemq-5.17.3-bin.tar.gz "http://www.apache.org/dyn/closer.cgi?filename=/activemq/5.17.3/apache-activemq-5.17.3-bin.tar.gz&action=download"```
    - následne je potrebné daný súbor rozbaliť
- Spustenie Apache ActiveMQ
    - závislosti od systému prejdeme do nasledovného priečinku
        - Linux ```$ cd apache-activemq-5.17.3/bin/```
        - Windows ```cd apache-activemq-5.17.3/bin/win64```
    - v terminály vo vyššie uvedenom priečinku spustíme Apache ActiveMQ
        - Linux ```$ ./activemq start```
        - Windows ```activemq start```
- Otvorenie Webového rozhrania 
    - ak všetko prebehlo úspešne mali by sme byť schopný otvoriť rozhranie na adrese http://localhost:8161/ do ktorého sa prihlásime zadaním mena "admin" a hesla "admin"
- Vytvorenie Queue a Topic 
    - vo wébovom rozhraní klikneme na "Queue" v hornej lište
    - a zadáme názov našej fronty "queue-1" (ak použijete iný názov je potrebné zmeniť destináciu v kóde)
    - ![Alt text](images/img.png?raw=true "queue")
    - rovnako postupuje aj pri pridaní nového! topic s názvom "topic-1"
    - ![Alt text](images/img_1.png?raw=true "topic")
- Import knižnice stomp.py do nášho IDE
    - knižnicu tohto komunikačného protokolu nájdeme na oficiálnej stránke [Pypi](https://pypi.org/project/stomp.py/) a importujeme túto knižnicu do nášho IDE.

---

## Architecture

### Message Broker
- poskytuje efektívnu komunikáciu a koordináciu medzi mikroservisami. 
- obsahuje buffer ktorý ukladá správy ktoré budú odovzdané príslušným mikroservisom
- tieto správy môžu byť requesty, errory, logy...
- odosielateľ tejto správy sa nazýva "producer" alebo "publisher" a prímateľ správy sa nazýva "consumer" alebo "subscriber" v závislosti od použitého bufferu.

### Buffer Types
- Oba buffre sú vlastne "miesta", kam producer alebo publisher posiela správy na ďalšie spracovanie. Jediný a hlavný rozdiel je len v tom, kto a ako tieto správy príme.
- #### Queue
  - môžu používať viacerí klienti na odosielanie a prijímanie správ, avšak každá správa je spracovaná iba raz, a to odoslaním práve jednému klientovi.
  - odosielateľ správy je „producer“ a prijímateľ je „consumer“.
  - ![Alt text](images/queue_diagram.png?raw=true "queue_diagram")
- #### Topic
  - môže rovnakú správu prijať viacero klientov.
  - klienti, ktorí si želajú prijať danú správu, informujú message brokera o tom, že by chceli dať "subscribe" k danému topicu. 
  - vždy, keď klient pošle správu na daný topic, message broker rozošle správu všetkým klientom, ktorí na nej majú "subscribe".
  - odosielateľ správy je „publisher“ a prijímateľ je „subscriber“.
  - ![Alt text](images/topic_diagram.png?raw=true "topic_diagram")

---

## Usage Example

- vytvoril som dvoch klientov [publisher](publisher_producer.py) a [subscriber](subscriber_consumer.py) pri destinácií nastavenej na topic prípadne [producer](publisher_producer.py) a [consumer](subscriber_consumer.py) pri destinácií queue.
- ako komunikačný protokol je použitý STOMP z knižnice stomp.py
- najskôr musíme zabezpečiť pripojenie k Apache ActiveMQ bežiaci na našom localhoste. Pre protokol STOMP stačí zavolať nasledovné riadky a zadefinovať meno a heslo.
- ```python
  import time
  import stomp
  conn = stomp.Connection()
  conn.connect(login="admin", passcode="admin")
  ```
- následne si musíme zvoliť aký typ buffera má message broker použiť na spravocanie našej správy v tomto jednoduchom príklade stačí zmeniť premennú "destination"
- #### Queue
  - ```python
    destination = "/queue/queue-1"
    ```
- #### Topic
  - ```python
    destination = "/topic/topic-1"
    ```

- #### Code Publisher/Producer
  - správy se posielajú metódou send(), ktorej parametrami sú destinácia, message, persistent čo je optional param ktorý hovorí o tom či sa má daná správa uložiť do databázy alebo nie.
  - ```python
       for i in range(0, MESSAGES):
           message = "This is message number #{i}!".format(i=i)
           conn.send(destination, message, persistent='true')
- #### Code Subscriber/Consumer
  - musíme zadefinovať callback metódy (spracovanie správy, informácie o chybe)
  - ```python
       class MsgListener(stomp.ConnectionListener):
           def on_error(self, message):
               print('received an error "%s"' % message.body)

           def on_message(self, frame):
               print('received a message "%s"' % frame.body)
  - registrovať nami vytvorený listener do protokolu
  - ```python
       conn.set_listener('stomp_listener', MsgListener())
  - a samozrejme musíme dať "subscribe" danému bufferu. Podľa tohto buffera (destination) message broker bude spracovávať našu správu jedným z opísaných spôsobov
  - ```python
       conn.subscribe(id='simple_listener', destination=destination, ack='auto')

---

## Summary

S knižnicou stomp.py je skutočne jednoduché pracovať s klientami v ActiveMQ. Na serveri ActiveMQ špeciálne v jej wébovom prostredí môžeme vytvoriť toľko queues a topics, koľko chceme, a komunikovať s nimi prostredníctvom rôznych klientov.

Ak by som niekedy rozmýšlal o rozdelení monolitnej aplikácie na architektúru mikroservisov, určite by som si spomenul na message brokera ako je ActiveMQ. Túto skúsenosť teda hodnotím kladne.
