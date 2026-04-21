# 📚 Plateforme d'Apprentissage en Ligne

A Django REST backend for an online learning platform — managing users, courses, modules, exercises and certifications.

![Python](https://img.shields.io/badge/Python-3.13-blue) ![Django](https://img.shields.io/badge/Django-5.x-green) ![Status](https://img.shields.io/badge/Status-In%20Progress-orange)

---

## Overview

Backend of a full-stack online learning platform built with Django. It covers role-based user management (teacher, student, admin), course and module creation, exercises, enrollment tracking and certificate generation.

---

## Architecture

```
Utilisateur
├── Enseignant     →  creates  →  Cours
│                                   └── Module  →  Exercice
├── Apprenant      →  enrolls via  →  Inscription  →  Certification
└── Administrateur
```

---

## Features

- **Role-based users** — Enseignant, Apprenant, Administrateur with a shared email-based login
- **Course management** — courses contain ordered modules with typed content
- **Exercises** — linked to modules with difficulty levels and minimum score
- **Enrollments & certifications** — tracks student progression and auto-generates a unique certificate on completion
- **Django admin panel** — full data management interface

---

## Project Status

| Phase | Status |
|---|---|
| UML design & architecture | ✅ |
| Django setup & custom user model | ✅ |
| All models (8 classes) | ✅ |
| REST views & routing | ✅ |
| Admin panel | ✅ |
| Token authentication | 🔲 |
| Frontend integration | 🔲 |

---

## Stack

`Python 3.13` · `Django 5.x` · `SQLite`
