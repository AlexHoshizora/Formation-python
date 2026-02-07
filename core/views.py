from django.shortcuts import render, redirect
from django.db.utils import OperationalError
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from .models import Enrollment, Progress

def home(request):
    # Si l'utilisateur a déjà une session d'inscription, on l'envoie directement vers l'espace
    if request.session.get("enrollment_id"):
        return redirect("dashboard")
    return render(request, "core/index.html")

def programme(request):
    return render(request, "core/programme.html")

def paiement(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if first_name and last_name and email and password:
            try:
                enrollment = Enrollment.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    amount=199,
                )
                # progression initiale : aucun module validé
                Progress.objects.create(enrollment=enrollment, last_module=0, last_section="")

                # e-mail de confirmation (fonctionnera une fois l’email backend configuré)
                try:
                    send_mail(
                        subject="Confirmation de création de votre compte – AG Formation",
                        message=(
                            f"Bonjour {first_name},\n\n"
                            "Votre compte AG Formation a bien été créé.\n"
                            "Vous pouvez maintenant accéder à votre espace de formation.\n\n"
                            "À très vite,\nAlex Gueydan"
                        ),
                        from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                        recipient_list=[email],
                        fail_silently=True,
                    )
                except Exception:
                    # on ignore les erreurs d’envoi ici
                    pass

                # “connexion” simple via la session
                request.session["enrollment_id"] = enrollment.id
                request.session["enrollment_first_name"] = enrollment.first_name

                return redirect("dashboard")

            except OperationalError:
                # Base non migrée ou table manquante
                return render(request, "core/paiement.html", {"db_error": True})

    return render(request, "core/paiement.html")

def contact(request):
    return render(request, "core/contact.html")

def connexion(request):
    return render(request, "core/connexion.html")

def dashboard(request):
    enrollment_id = request.session.get("enrollment_id")
    if not enrollment_id:
        return redirect("connexion")

    try:
        enrollment = Enrollment.objects.get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        return redirect("connexion")

    # progression associée (créée lors du paiement)
    progress = getattr(enrollment, "progress", None)
    total_modules = 11  # modules 0 à 10
    last_module = progress.last_module if progress else 0
    progress_percent = int(last_module / (total_modules - 1) * 100) if total_modules > 1 else 0

    modules = [
        {
            "number": 0,
            "title": "Découvrir Python et installer tout ce qu’il faut",
            "sections": [
                {
                    "slug": "installation-python",
                    "title": "Installer Python 3",
                    "url": reverse("module_0_installation"),
                },
                {
                    "slug": "installation-editeur",
                    "title": "Installer et préparer votre éditeur",
                    "url": "#",
                },
                {
                    "slug": "scripts-vs-console",
                    "title": "Script Python vs console interactive",
                    "url": "#",
                },
                {
                    "slug": "premier-programme",
                    "title": "Votre premier programme",
                    "url": "#",
                },
            ],
        },
        {
            "number": 1,
            "title": "Manipuler des nombres et des textes",
            "sections": [
                {"slug": "variables", "title": "Vos premières variables", "url": "#"},
                {"slug": "input", "title": "Poser une question à l’utilisateur", "url": "#"},
            ],
        },
        {
            "number": 2,
            "title": "Prendre des décisions dans votre code",
            "sections": [
                {"slug": "conditions", "title": "Découvrir if / elif / else", "url": "#"},
                {"slug": "menus", "title": "Créer un petit menu texte", "url": "#"},
            ],
        },
        {
            "number": 3,
            "title": "Répéter des actions et gérer des listes",
            "sections": [
                "Boucles for et while",
                "Créer et modifier des listes",
                "Découvrir les dictionnaires",
                "Parcourir une liste et calculer un total",
            ],
        },
        {
            "number": 4,
            "title": "Découper votre code en fonctions réutilisables",
            "sections": [
                "Créer vos premières fonctions",
                "Donner de bons noms de fonctions",
                "Réutiliser une fonction dans plusieurs scripts",
                "Organiser un fichier en petites briques",
            ],
        },
        {
            "number": 5,
            "title": "Comprendre ce qui se passe dans les coulisses",
            "sections": [
                "Types immuables vs mutables",
                "Comprendre les références en mémoire",
                "Éviter les copies piégées de listes",
                "Corriger des bugs liés à la mutabilité",
            ],
        },
        {
            "number": 6,
            "title": "Ne plus paniquer devant les messages d’erreur",
            "sections": [
                "Lire un traceback Python",
                "Utiliser try / except intelligemment",
                "Gérer les mauvaises saisies utilisateur",
                "Afficher des messages d’erreur clairs",
            ],
        },
        {
            "number": 7,
            "title": "Lire et écrire dans des fichiers",
            "sections": [
                "Ouvrir et parcourir un fichier texte",
                "Lire et écrire des fichiers CSV",
                "Utiliser le mot-clé with pour les fichiers",
                "Générer un rapport automatiquement",
            ],
        },
        {
            "number": 8,
            "title": "Organiser vos données comme des objets",
            "sections": [
                "Créer votre première classe",
                "Ajouter attributs et méthodes",
                "Instancier plusieurs objets",
                "Quand utiliser la POO",
            ],
        },
        {
            "number": 9,
            "title": "Écrire du code lisible et propre",
            "sections": [
                "Organiser un projet en modules",
                "Suivre les conventions PEP 8",
                "Renommer un script pour plus de clarté",
                "Ajouter des commentaires utiles",
            ],
        },
        {
            "number": 10,
            "title": "Réaliser vos projets de fin de parcours",
            "sections": [
                "Construire un petit jeu en ligne de commande",
                "Créer un mini gestionnaire (tâches, livres…)",
                "Mettre en place un script d’automatisation",
                "Préparer vos futurs projets personnels",
            ],
        },
    ]

    context = {
        "enrollment": enrollment,
        "progress": progress,
        "last_module": last_module,
        "progress_percent": progress_percent,
        "modules": modules,
    }
    return render(request, "core/dashboard.html", context)


def module_0_installation(request):
    modules = [
        {
            "number": 0,
            "title": "Découvrir Python et installer tout ce qu’il faut",
            "sections": [
                {
                    "slug": "installation-python",
                    "title": "Installer Python 3",
                    "url": reverse("module_0_installation"),
                },
                {
                    "slug": "installation-editeur",
                    "title": "Installer et préparer votre éditeur",
                    "url": "#",
                },
                {
                    "slug": "scripts-vs-console",
                    "title": "Script Python vs console interactive",
                    "url": "#",
                },
                {
                    "slug": "premier-programme",
                    "title": "Votre premier programme",
                    "url": "#",
                },
            ],
        },
        {
            "number": 1,
            "title": "Manipuler des nombres et des textes",
            "sections": [
                {"slug": "variables", "title": "Vos premières variables", "url": "#"},
                {"slug": "input", "title": "Poser une question à l’utilisateur", "url": "#"},
            ],
        },
        {
            "number": 2,
            "title": "Prendre des décisions dans votre code",
            "sections": [
                {"slug": "conditions", "title": "Découvrir if / elif / else", "url": "#"},
                {"slug": "menus", "title": "Créer un petit menu texte", "url": "#"},
            ],
        },
        {
            "number": 3,
            "title": "Répéter des actions et gérer des listes",
            "sections": [
                "Boucles for et while",
                "Créer et modifier des listes",
                "Découvrir les dictionnaires",
                "Parcourir une liste et calculer un total",
            ],
        },
        {
            "number": 4,
            "title": "Découper votre code en fonctions réutilisables",
            "sections": [
                "Créer vos premières fonctions",
                "Donner de bons noms de fonctions",
                "Réutiliser une fonction dans plusieurs scripts",
                "Organiser un fichier en petites briques",
            ],
        },
        {
            "number": 5,
            "title": "Comprendre ce qui se passe dans les coulisses",
            "sections": [
                "Types immuables vs mutables",
                "Comprendre les références en mémoire",
                "Éviter les copies piégées de listes",
                "Corriger des bugs liés à la mutabilité",
            ],
        },
        {
            "number": 6,
            "title": "Ne plus paniquer devant les messages d’erreur",
            "sections": [
                "Lire un traceback Python",
                "Utiliser try / except intelligemment",
                "Gérer les mauvaises saisies utilisateur",
                "Afficher des messages d’erreur clairs",
            ],
        },
        {
            "number": 7,
            "title": "Lire et écrire dans des fichiers",
            "sections": [
                "Ouvrir et parcourir un fichier texte",
                "Lire et écrire des fichiers CSV",
                "Utiliser le mot-clé with pour les fichiers",
                "Générer un rapport automatiquement",
            ],
        },
        {
            "number": 8,
            "title": "Organiser vos données comme des objets",
            "sections": [
                "Créer votre première classe",
                "Ajouter attributs et méthodes",
                "Instancier plusieurs objets",
                "Quand utiliser la POO",
            ],
        },
        {
            "number": 9,
            "title": "Écrire du code lisible et propre",
            "sections": [
                "Organiser un projet en modules",
                "Suivre les conventions PEP 8",
                "Renommer un script pour plus de clarté",
                "Ajouter des commentaires utiles",
            ],
        },
        {
            "number": 10,
            "title": "Réaliser vos projets de fin de parcours",
            "sections": [
                "Construire un petit jeu en ligne de commande",
                "Créer un mini gestionnaire (tâches, livres…)",
                "Mettre en place un script d’automatisation",
                "Préparer vos futurs projets personnels",
            ],
        },
    ]

    context = {
        "modules": modules,
        "current_module": 0,
        "current_section": "installation-python",
    }
    return render(request, "core/module_0_installation.html", context)