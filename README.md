# 🌉 Nirman Setu Core

> **Bridging citizens with the government schemes they are eligible for.**

Nirman Setu Core is an AI-assisted platform designed to help citizens—especially farmers and rural communities—discover relevant government welfare schemes, understand their eligibility, receive proactive notifications, and simplify the application process through conversational assistance and intelligent form filling.

---

# 🚨 The Problem

Government welfare schemes are created to support farmers, students, workers, and other eligible citizens.

However, many eligible people never receive these benefits.

### Why?

* Citizens are not proactively informed about schemes relevant to them.
* Government Resolutions (GRs) and scheme information can be difficult to understand.
* Eligibility requirements are often complex.
* Information is scattered across multiple government portals.
* Language and digital literacy can become barriers.
* Application forms can be difficult and repetitive.
* Citizens often don't know which schemes they are eligible for.

As a result, many eligible beneficiaries remain unaware of opportunities that were specifically created for them.

---

# 💡 Our Solution

**Nirman Setu acts as a digital bridge between citizens and government welfare schemes.**

Instead of requiring users to manually search through multiple government portals, the platform aims to understand a user's profile and match it with relevant schemes.

The system is designed to:

* 🤖 Interact with citizens through an AI chatbot.
* 🧾 Collect relevant information through natural conversation.
* 🔍 Identify schemes a citizen may be eligible for.
* 🔔 Notify users about relevant schemes and opportunities.
* 📖 Explain complex scheme information in simpler language.
* 📝 Assist users in filling application forms.
* 🌐 Support regional and accessible communication.
* 🛡️ Reduce unnecessary storage of sensitive documents.

---

# 🎯 Primary Focus

The initial focus of Nirman Setu is to help **farmers and rural citizens** become more aware of government schemes relevant to them.

A farmer should not need to visit multiple websites and manually search for every possible scheme.

The goal is to create a simpler journey:

```text
Farmer
   │
   ▼
🤖 Talks with Nirman Setu
   │
   ▼
Provides Basic Information
   │
   ▼
🔍 System Identifies Relevant Schemes
   │
   ▼
🔔 Farmer Gets Notified
   │
   ▼
📖 Understands the Scheme
   │
   ▼
📝 Gets Assistance with Form Filling
```

---

# 🔔 Proactive Scheme Awareness

Most existing systems depend on the citizen searching for schemes.

Nirman Setu aims to reverse this process.

Instead of:

> **Citizen → Searches for Scheme**

The approach is:

> **User Profile → Relevant Scheme Identified → User Notified**

This means that when a relevant scheme is available, the platform can help bring that information directly to the eligible citizen.

---

# 🤖 AI-Powered Conversational Assistance

Nirman Setu is designed around a simple conversational experience.

Instead of immediately presenting users with complex forms, the platform can collect information step-by-step through a chatbot.

The AI assistant can help users:

* Understand what information is required.
* Answer eligibility-related questions.
* Simplify complex scheme information.
* Guide users through the application process.
* Assist in filling available form fields.

The goal is to make interacting with government services feel less like navigating multiple complicated portals and more like asking for assistance.

---

# 🔍 Intelligent Eligibility Matching

At the core of Nirman Setu is the concept of an **eligibility matching system**.

Each government scheme has different requirements, such as:

* Age
* Income
* Occupation
* State or district
* Category
* Land ownership
* Education
* Other scheme-specific requirements

The system is planned to compare a user's available profile information against these requirements and identify potentially relevant schemes.

```text
                 USER PROFILE
                       │
                       ▼
              ┌────────────────┐
              │ Income         │
              │ Occupation     │
              │ Location       │
              │ Age            │
              │ Category       │
              │ Other Details  │
              └───────┬────────┘
                      │
                      ▼
             ELIGIBILITY MATCHING
                      │
                      ▼
              RELEVANT SCHEMES
                      │
                      ▼
             🔔 USER NOTIFIED
```

---

# 📝 Application and Form Filling Assistance

Discovering a scheme is only the first step.

Many citizens may still face difficulty while completing the application process.

Nirman Setu aims to assist users by:

* Explaining what each form field means.
* Reusing information already provided by the user where appropriate.
* Helping reduce repetitive data entry.
* Guiding users through the application journey.
* Redirecting or integrating with official application systems where supported.

The user should always be able to review and confirm information before proceeding.

---

# 👥 Platform Concept

Nirman Setu is planned around two major sides of the platform.

## 👤 User Side

Designed for citizens and beneficiaries.

### Planned Features

* AI-powered chatbot
* User profile creation
* Personalized scheme discovery
* Eligibility checking
* Scheme awareness and notifications
* Simple explanation of schemes and GRs
* Application assistance
* Form filling support
* Application status tracking

---

## 🛠️ Admin Side

Designed to manage the scheme ecosystem.

### Planned Features

* Add and manage government schemes
* Update scheme information
* Define eligibility requirements
* Activate or deactivate schemes
* Manage scheme categories
* Monitor applications and activity
* View platform-level insights

The admin side will allow new schemes and eligibility requirements to be managed without changing the entire platform experience for users.

---

# 🏗️ High-Level Architecture

```text
                    ┌───────────────────┐
                    │       USERS       │
                    │                   │
                    │ Farmers / Citizens│
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   NIRMAN SETU     │
                    │                   │
                    │ AI Conversation   │
                    │ Profile Building  │
                    │ Scheme Discovery  │
                    └─────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
       ┌─────────────┐ ┌─────────────┐ ┌──────────────┐
       │ AI / Chatbot│ │ Eligibility │ │ Notification │
       │ Assistance  │ │  Matching   │ │    System    │
       └─────────────┘ └─────────────┘ └──────────────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Scheme & User Data│
                    └───────────────────┘
```

---

# 🔄 Planned User Workflow

```text
                 USER STARTS
                      │
                      ▼
              🤖 AI ASSISTANT
                      │
                      ▼
            USER SHARES DETAILS
                      │
                      ▼
             PROFILE IS CREATED
                      │
                      ▼
            🔍 SCHEME DISCOVERY
                      │
                      ▼
            ELIGIBLE / RELEVANT
                 SCHEMES FOUND
                      │
                      ▼
              🔔 USER NOTIFIED
                      │
                      ▼
             📖 SCHEME EXPLAINED
                      │
                      ▼
             📝 FORM ASSISTANCE
                      │
                      ▼
                NEXT STEPS
```

---

# 🔐 Privacy-First Approach

Nirman Setu is designed with the principle of minimizing unnecessary storage of sensitive information.

The planned approach is to:

* Store only information required for the platform's functionality.
* Avoid unnecessary central storage of sensitive identity documents.
* Explore verified digital document infrastructure where appropriate.
* Keep the user in control of information used during the application process.

Privacy and security will be important considerations as the project develops.

---

# 🛠️ Planned Technology Stack

The project is currently in its planning and development stage.

The proposed technology stack includes:

| Area                      | Planned Technology            |
| ------------------------- | ----------------------------- |
| Frontend                  | React / Next.js               |
| Backend                   | Node.js + Express             |
| Database                  | PostgreSQL                    |
| AI Assistance             | Gemini API                    |
| Eligibility Matching      | Rule-Based Eligibility Engine |
| Authentication            | Phone / OTP                   |
| Regional Language & Voice | Bhashini                      |
| Notifications             | WhatsApp / SMS                |
| Document Verification     | DigiLocker Integration        |
| Deployment                | Cloud-Based Infrastructure    |

> The technology choices and implementation may evolve as the project develops.

---

# 🌱 Future Scope

* 🎙️ Voice-first interaction
* 🌐 Support for more regional languages
* 📱 WhatsApp-based access
* 🔔 Personalized real-time notifications
* 🗺️ State-specific scheme discovery
* 📊 Analytics dashboard
* 📄 AI-assisted understanding of Government Resolutions (GRs)
* 🤝 Integration with additional government digital services
* 🧠 Improved personalized scheme recommendations
* 📱 Better accessibility for low-end and shared devices

---

# 🎯 Vision

> **A citizen should not miss a government benefit simply because they did not know where to search or how to apply.**

Nirman Setu aims to bridge the gap between **government welfare opportunities** and the **citizens they are meant to support**.

The long-term vision is a platform where discovering opportunities, understanding eligibility, receiving notifications, and getting assistance with applications becomes significantly simpler.

---

# 🌉 Nirman Setu

### **Discover. Understand. Apply.**

> *Building a digital bridge between citizens and the opportunities they are entitled to.*
