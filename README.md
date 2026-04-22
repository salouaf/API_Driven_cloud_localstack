------------------------------------------------------------------------------------------------------
ATELIER API-DRIVEN INFRASTRUCTURE
------------------------------------------------------------------------------------------------------
L’idée en 30 secondes : **Orchestration de services AWS via API Gateway et Lambda dans un environnement émulé**.  
Cet atelier propose de concevoir une architecture **API-driven** dans laquelle une requête HTTP déclenche, via **API Gateway** et une **fonction Lambda**, des actions d’infrastructure sur des **instances EC2**, le tout dans un **environnement AWS simulé avec LocalStack** et exécuté dans **GitHub Codespaces**. L’objectif est de comprendre comment des services cloud serverless peuvent piloter dynamiquement des ressources d’infrastructure, indépendamment de toute console graphique.Cet atelier propose de concevoir une architecture API-driven dans laquelle une requête HTTP déclenche, via API Gateway et une fonction Lambda, des actions d’infrastructure sur des instances EC2, le tout dans un environnement AWS simulé avec LocalStack et exécuté dans GitHub Codespaces. L’objectif est de comprendre comment des services cloud serverless peuvent piloter dynamiquement des ressources d’infrastructure, indépendamment de toute console graphique.
  
-------------------------------------------------------------------------------------------------------
Séquence 1 : Codespace de Github
-------------------------------------------------------------------------------------------------------
Objectif : Création d'un Codespace Github  
Difficulté : Très facile (~5 minutes)
-------------------------------------------------------------------------------------------------------
RDV sur Codespace de Github : <a href="https://github.com/features/codespaces" target="_blank">Codespace</a> **(click droit ouvrir dans un nouvel onglet)** puis créer un nouveau Codespace qui sera connecté à votre Repository API-Driven.
  
---------------------------------------------------
Séquence 2 : Création de l'environnement AWS (LocalStack)
---------------------------------------------------
Objectif : Créer l'environnement AWS simulé avec LocalStack  
Difficulté : Simple (~5 minutes)
---------------------------------------------------

Dans le terminal du Codespace copier/coller les codes ci-dessous etape par étape :  

**Installation de l'émulateur LocalStack**  
```
sudo -i mkdir rep_localstack
```
```
sudo -i python3 -m venv ./rep_localstack
```
```
sudo -i pip install --upgrade pip && python3 -m pip install localstack && export S3_SKIP_SIGNATURE_VALIDATION=0
```
```
localstack start -d
```
**vérification des services disponibles**  
```
localstack status services
```
**Réccupération de l'API AWS Localstack** 
Votre environnement AWS (LocalStack) est prêt. Pour obtenir votre AWS_ENDPOINT cliquez sur l'onglet **[PORTS]** dans votre Codespace et rendez public votre port **4566** (Visibilité du port).
Réccupérer l'URL de ce port dans votre navigateur qui sera votre ENDPOINT AWS (c'est à dire votre environnement AWS).
Conservez bien cette URL car vous en aurez besoin par la suite.  

Pour information : IL n'y a rien dans votre navigateur et c'est normal car il s'agit d'une API AWS (Pas un développement Web type UX).

---------------------------------------------------
Séquence 3 : Exercice
---------------------------------------------------
Objectif : Piloter une instance EC2 via API Gateway
Difficulté : Moyen/Difficile (~2h)
---------------------------------------------------  
Votre mission (si vous l'acceptez) : Concevoir une architecture **API-driven** dans laquelle une requête HTTP déclenche, via **API Gateway** et une **fonction Lambda**, lancera ou stopera une **instance EC2** déposée dans **environnement AWS simulé avec LocalStack** et qui sera exécuté dans **GitHub Codespaces**. [Option] Remplacez l'instance EC2 par l'arrêt ou le lancement d'un Docker.  

**Architecture cible :** Ci-dessous, l'architecture cible souhaitée.   
  
![Screenshot Actions](API_Driven.png)   
  
---------------------------------------------------  
## Processus de travail (résumé)

1. Installation de l'environnement Localstack (Séquence 2)
2. Création de l'instance EC2
3. Création des API (+ fonction Lambda)
4. Ouverture des ports et vérification du fonctionnement

---------------------------------------------------
Séquence 4 : Documentation  
Difficulté : Facile (~30 minutes)
---------------------------------------------------
**Complétez et documentez ce fichier README.md** pour nous expliquer comment utiliser votre solution.  
Faites preuve de pédagogie et soyez clair dans vos expliquations et processus de travail.  
   
---------------------------------------------------
Evaluation
---------------------------------------------------
Cet atelier, **noté sur 20 points**, est évalué sur la base du barème suivant :  
- Repository exécutable sans erreur majeure (4 points)
- Fonctionnement conforme au scénario annoncé (4 points)
- Degré d'automatisation du projet (utilisation de Makefile ? script ? ...) (4 points)
- Qualité du Readme (lisibilité, erreur, ...) (4 points)
- Processus travail (quantité de commits, cohérence globale, interventions externes, ...) (4 points) 

---------------------------------------------------
## Ma Solution
---------------------------------------------------

### Ce que j'ai construit

Une architecture API-driven complète :
Requête HTTP → API Gateway → Lambda → EC2 (start/stop)

### Étapes réalisées

**1. Création de l'instance EC2**
```python
# Créer une instance EC2 dans LocalStack
ec2 = boto3.client('ec2', endpoint_url='http://localhost:4566', region_name='us-east-1', aws_access_key_id='test', aws_secret_access_key='test')
ec2.run_instances(ImageId='ami-07b643b5e45e', InstanceType='t2.micro', MinCount=1, MaxCount=1)
# Instance créée : i-f5a5df153f11d2641
```

**2. Création de la fonction Lambda**

La Lambda reçoit l'action (`start` ou `stop`) et pilote l'instance EC2 :
```python
def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    instance_id = body.get('instance_id')
    action = body.get('action')
    if action == "start":
        ec2.start_instances(InstanceIds=[instance_id])
        return {"statusCode": 200, "body": json.dumps({"message": f"Instance {instance_id} démarrée"})}
    elif action == "stop":
        ec2.stop_instances(InstanceIds=[instance_id])
        return {"statusCode": 200, "body": json.dumps({"message": f"Instance {instance_id} arrêtée"})}
```

**3. Création de l'API Gateway**

L'API Gateway expose un endpoint HTTP POST `/ec2` connecté à la Lambda.

**4. Ouverture du port 4566**

Dans l'onglet PORTS du Codespace, rendre le port 4566 public pour obtenir l'URL publique.

---

### Comment utiliser la solution

**Arrêter l'instance EC2 :**
```bash
curl -X POST "https://bookish-carnival-g4vrq7prjwxwcvqw-4566.app.github.dev/_aws/execute-api/otwmmt3szx/prod/ec2" \
  -H "Content-Type: application/json" \
  -d '{"instance_id": "i-f5a5df153f11d2641", "action": "stop"}'
```

**Démarrer l'instance EC2 :**
```bash
curl -X POST "https://bookish-carnival-g4vrq7prjwxwcvqw-4566.app.github.dev/_aws/execute-api/otwmmt3szx/prod/ec2" \
  -H "Content-Type: application/json" \
  -d '{"instance_id": "i-f5a5df153f11d2641", "action": "start"}'
```

**Réponses attendues :**
```json
{"message": "Instance i-f5a5df153f11d2641 arrêtée"}
{"message": "Instance i-f5a5df153f11d2641 démarrée"}
```

---

### Points importants

- L'URL publique du port 4566 change à chaque redémarrage du Codespace
- LocalStack ne persiste pas après redémarrage — recréer EC2, Lambda et API Gateway
- La Lambda utilise `172.17.0.1:4566` au lieu de `localhost:4566` car elle tourne dans Docker


### Auteur

Salouaf - Atelier API-Driven Infrastructure

