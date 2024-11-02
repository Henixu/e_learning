from django.db import models
from django.contrib.auth.models import AbstractUser

# Modèle personnalisé pour l'utilisateur
class User(AbstractUser):
    # Ajout des champs spécifiques à la plateforme
    niveau = models.CharField(max_length=50, choices=[('débutant', 'Débutant'), ('intermédiaire', 'Intermédiaire'), ('avancé', 'Avancé')])
    preferences = models.JSONField(null=True, blank=True)
    date_inscription = models.DateField(auto_now_add=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='megan_user_set',  # Add a custom related_name
        blank=True,
        help_text='The groups this user belongs to.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='megan_user_permissions_set',  # Add a custom related_name
        blank=True,
        help_text='Specific permissions for this user.'
    )

# Catégorie de cours
class Category(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

# Modèle pour les cours
class Course(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField()
    niveau_difficulte = models.CharField(max_length=50, choices=[('débutant', 'Débutant'), ('intermédiaire', 'Intermédiaire'), ('avancé', 'Avancé')])
    date_creation = models.DateField(auto_now_add=True)
    categorie = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")

    def __str__(self):
        return self.titre

# Suivi des progrès de l'utilisateur dans un cours
class UserProgress(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="progress")
    cours = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="progress")
    progression = models.IntegerField(default=0)  # Progression en %
    date_dernier_acces = models.DateField(auto_now=True)
    statut = models.CharField(max_length=50, choices=[('en cours', 'En Cours'), ('terminé', 'Terminé'), ('échoué', 'Échoué')])

    def __str__(self):
        return f"{self.utilisateur.username} - {self.cours.titre} - {self.progression}%"

# Modèle pour les quiz liés à un cours
class Quiz(models.Model):
    cours = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="quizzes")
    question = models.TextField()
    choix = models.JSONField()  # Les choix possibles
    reponse_correcte = models.CharField(max_length=255)

    def __str__(self):
        return f"Quiz pour {self.cours.titre}"

# Résultats des quiz pour chaque utilisateur
class QuizResult(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_results")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="results")
    score = models.IntegerField()
    date_quiz = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.quiz.cours.titre} - {self.score}"

# Recommandations basées sur l'IA
class Recommendation(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations")
    type_recommendation = models.CharField(max_length=50, choices=[('cours', 'Cours'), ('article', 'Article'), ('vidéo', 'Vidéo'), ('quiz', 'Quiz')])
    contenu = models.TextField()
    date_recommandation = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Recommandation pour {self.utilisateur.username}"
