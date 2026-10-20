# ERT INVENTORY — prototype Android V1

Prototype Flutter **hors-ligne** fondé sur `INVENTAIRES & CONTRÔLES DU PARC VEHICULES V2.pdf` (20 octobre 2026).

## Ce qui est réellement implémenté

- Accueil des **7 véhicules retenus** : VSAV, FPT, VPSID, VRE, CCFM, VIM, CCFL 1. **CCFL 2 est exclu**.
- **VSAV uniquement opérationnel en V1** : ses **18 compartiments et 103 lignes de matériel** sont dans `assets/catalog.json`, pages 3–16 du PDF. Les six autres véhicules sont visibles, mais leur inventaire n'est pas encore intégré.
- Saisie libre du nom/prénom de l'agent, choix `VÉRIFICATION` ou `INVENTAIRE`.
- Contrôles généraux : jauge carburant, voyants de tableau de bord, carrosserie; en inventaire, jauge O₂ B5 et détecteur CO.
- Contrôle individualisé de chaque équipement avec état non vérifié / conforme / anomalie; bouton **Nothing to report** par compartiment.
- Anomalies documentées : type, quantité présente, observation **obligatoire**, plusieurs photos appareil photo / galerie.
- Sauvegarde automatique et reprise d'un contrôle en cours, historique local, registre local d'anomalies avec regroupement des signalements répétés et statuts.
- Export PDF du contrôle avec photos (si les fichiers existent encore), **partage manuel** via la feuille de partage Android, permettant de choisir Outlook.
- Lecture **dans l'application** des QR codes portant `ERTINV:VSAV`, etc. Les QR codes imprimables figurent dans un PDF séparé.
- Menu admin avec code local de démonstration; permet de modifier/ajouter/désactiver des équipements et changer le statut des anomalies sur **ce téléphone**.

## Ce qui n'est PAS encore opérationnel

- **APK compilé** : le projet est livré sous forme de sources. Aucun SDK Android ou Flutter n'est disponible dans l'environnement de création ; l'APK doit être compilé.
- **Partage de données entre les 27 agents** : aucun serveur ni synchronisation n'est configuré. Chaque téléphone possède ses propres données, contrôles, photos et code admin.
- **Envoi automatique** via Outlook / Power Automate : l'application **prépare un PDF à partager** ; l'utilisateur choisit Outlook et confirme l'envoi. Ce n'est pas un envoi automatique et l'app ne connaît pas le statut de livraison.
- Authentification/autorisation administrateur robuste : le code local ne garantit aucune sécurité à l'échelle d'une équipe. Une authentification Microsoft Entra ID ou un autre fournisseur avec règles côté serveur sera nécessaire.
- QR code ouvrant l'application depuis l'appareil photo standard : le scanner QR de la V1 s'ouvre **dans** l'application. Les liens profonds nécessiteraient une configuration Android complémentaire.
- Suivi centralisé des échéances, notifications automatiques, intégration des six véhicules restants.

## Obtenir un APK via GitHub Actions (ordinateur, sans installer Android Studio)

1. Créer un **dépôt GitHub privé** (le catalogue contient des informations sur des équipements d'un site industriel).
2. Décompresser tous les fichiers de cette archive à la racine du dépôt, puis les envoyer sur la branche `main`.
3. Ouvrir l'onglet **Actions** > **Construire APK Android ERT** > **Run workflow**.
4. Le workflow installe Flutter, génère le squelette Android (`flutter create --platforms android --org org.ert .`), vérifie le code, puis construit un `app-debug.apk`.
5. Une fois terminé, télécharger l'artefact **ERT-Inventory-V1-APK**. Extraire son fichier `app-debug.apk`, puis l'installer sur un Android autorisant les applications depuis cette source.

Ce flux est destiné **aux tests**. Un déploiement sur les 27 téléphones demande un APK/AAB de publication signé, une politique de mises à jour et un socle sécurisé côté serveur.

## Compiler localement (si Flutter est installé)

```bash
flutter create --platforms android --org org.ert .
flutter pub get
flutter analyze
flutter run
# pour un APK de test :
flutter build apk --debug
```

## Inventaire et fidélité à la source

- `assets/catalog.json` contient les intitulés de matériels (103 lignes réparties en 18 compartiments), quantités uniquement lorsqu'explicites dans le PDF ; certains ensembles restent nommés comme dans la source.
- Les options de carrosserie spécifiques au **VSAV** sont pratiquement illisibles dans l'export PDF (p. 4) : en V1, la carrosserie est contrôlée **globalement** avec observation libre, plutôt que d'inventer des items.
- Les échéances dans le formulaire sont recopiées comme références historiques, pas comme des dates validées (ex. détecteur CO : novembre 2026).
- L'app peut enregistrer un contrôle **partiel**, mais affiche le nombre de points non vérifiés au lieu de déclarer à tort tout le contenu conforme.

## Données et confidentialité

Les photographies et l'historique sont stockés localement, sur le téléphone de l'agent. Avant usage opérationnel, valider avec l'organisation les autorisations de captation et stockage de photos, la politique BYOD, la rétention des données et le choix de l'hébergement. Ne pas transmettre des données de site sensibles via un service non autorisé.

## Structure

- `lib/main.dart` : écrans et interactions.
- `lib/core.dart` : sauvegarde locale, agrégation et génération PDF.
- `assets/catalog.json` : référentiel véhicules et VSAV.
- `.github/workflows/build-apk.yml` : compilation sur GitHub Actions.
- `make_data.py` : génération reproductible du référentiel VSAV.

