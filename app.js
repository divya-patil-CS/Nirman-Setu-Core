/* ========================================
   YOJANALINK - INTERNATIONALIZATION & APP LOGIC
   JavaScript for index.html, login.html, agree.html, info.html
   ======================================== */

// Translation data for all pages
const translations = {
  hi: {
    common: {
      welcome: "आपका स्वागत है",
      tagline: "आपकी योजनाओं का दुवा",
      headerNote: "सरकारी योजनाओं की जानकारी, अब आपकी भाषा में",
      continue: "आगे बढ़ें",
      listen: "सुनें",
      back: "वापस जाएँ",
      changeLanguage: "भाषा बदलें",
      trustMessage: "सरल • सुरक्षित • आपके लिए"
    },
    agreement: {
      title: "उपयोगकर्ता समझौता और सहमति",
      content: "\"YojanaLink\" में आपका स्वागत है, यह एक ऐसा मंच है जो आपको सरकारी योजनाएं, लाभ, अनुदान, सुविधाएं और अन्य उपयोगी सेवाएं खोजने में मदद करता है। प्रश्न पूछने, योजनाओं को समझने, मूल पात्रता की जांच करने और सरल भाषा में मार्गदर्शन पाने के लिए आप हमारे **चैटबॉट** का उपयोग कर सकते हैं। बेहतर सुझाव प्रदान करने के लिए, हम आपका नाम, मोबाइल नंबर, आयु, व्यवसाय, स्थान, शिक्षा और पारिवारिक जानकारी जैसे विवरण मांग सकते हैं। आपके मोबाइल नंबर को OTP के माध्यम से सत्यापित किया जा सकता है। आप अपने परिवार के सदस्यों के विवरण भी जोड़ सकते हैं ताकि उन्हें उपयोगी योजनाएं मिल सकें। भविष्य में, हम आपकी अनुमति से **आधार या डिजीलॉकर** का उपयोग करके पहचान सत्यापन और फॉर्म भरना आसान बनाने के लिए सेवाएं प्रदान कर सकते हैं। चैटबॉट द्वारा प्रदान की गई जानकारी मार्गदर्शन के लिए है और योजना की पात्रता या अनुमोदन की गारंटी नहीं दे सकती है। \"मैं सहमत हूँ और आगे बढ़ें\" पर क्लिक करके, आप सही जानकारी प्रदान करने और हमकी **गोपनीयता नीति और नियम व शर्तों** को स्वीकार करने के लिए सहमत हैं।",
      agreeContinue: "मैं सहमत हूँ और आगे बढ़ें"
    },
    language: {
      chooseLanguage: "अपनी भाषा चुनें",
      prompt: "अपने आराम की भाषा चुनें",
      optionsLabel: "भाषा चुनें",
      hindi: "हिंदी",
      marathi: "मराठी",
      english: "English",
      selectedMessage: "भाषा चुनी गई है।",
      futureMessage: "भाषा चुनी गई है। अगला चरण जल्द उपलब्ध होगा।"
    },
    login: {
      title: "लॉग इन करें",
      intro: "सरकारी योजनाओं की जानकारी पाने के लिए अपना मोबाइल नंबर दर्ज करें।",
      mobileNumber: "मोबाइल नंबर",
      mobilePlaceholder: "10 अंकों का मोबाइल नंबर",
      sendOtp: "ओटीपी भेजें",
      enterOtp: "ओटीपी दर्ज करें",
      otpPlaceholder: "6 अंकों का ओटीपी",
      verify: "सत्यापित करें",
      resendOtp: "ओटीपी फिर से भेजें",
      terms: "आगे बढ़कर आप सेवा की शर्तों से सहमत हैं।",
      otpSent: "आपके मोबाइल नंबर पर एक ओटीपी भेजा गया है।",
      verified: "मोबाइल नंबर सत्यापित है। अगला चरण जल्द उपलब्ध होगा।",
      invalidMobile: "कृपया सही 10 अंकों का मोबाइल नंबर दर्ज करें।",
      invalidOtp: "कृपया 6 अंकों का ओटीपी दर्ज करें।"
    },
    info: {
      title: "अपनी जानकारी भरें",
      intro: "आपके लिए सही योजनाएं खोजने के लिए अपनी जानकारी दर्ज करें।",
      fullName: "पूरा नाम",
      fullNamePlaceholder: "अपना पूरा नाम दर्ज करें",
      email: "ईमेल",
      emailPlaceholder: "अपना ईमेल दर्ज करें",
      location: "स्थान",
      locationPlaceholder: "अपना शहर या गांव दर्ज करें",
      phone: "मोबाइल नंबर",
      submit: "जानकारी जमा करें",
      saved: "आपकी जानकारी सफलतापूर्वक जमा हो गई है।",
      required: "कृपया सभी जानकारी भरें।"
    }
  },
  mr: {
    common: {
      welcome: "तुमचे स्वागत आहे",
      tagline: "तुमच्या योजनांचा दुवा",
      headerNote: "सरकारी योजनांची माहिती, आता तुमच्या भाषेत",
      continue: "पुढे चला",
      listen: "ऐकून घ्या",
      back: "मागे जा",
      changeLanguage: "भाषा बदला",
      trustMessage: "सोपे • सुरक्षित • तुमच्यासाठी"
    },
    agreement: {
      title: "वापरकर्ता करार आणि संमती",
      content: "\"योजनालिंक\" मध्ये आपले स्वागत आहे, हे एक असे व्यासपीठ आहे जे आपल्याला सरकारी योजना, लाभ, अनुदान, सुविधा आणि इतर उपयुक्त सेवा शोधण्यात मदत करते. प्रश्न विचारण्यासाठी, योजना समजून घेण्यासाठी, मूलभूत पात्रता तपासण्यासाठी आणि सोप्या भाषेत मार्गदर्शन मिळवण्यासाठी आपण आमच्या **चॅटबॉट**चा वापर करू शकता. अधिक चांगल्या सूचना देण्यासाठी, आम्ही आपले नाव, मोबाईल नंबर, वय, व्यवसाय, ठिकाण, शिक्षण आणि कौटुंबिक माहिती यांसारखा तपशील विचारू शकतो. आपला मोबाईल नंबर ओटीपीद्वारे सत्यापित केला जाऊ शकतो. आपण आपल्या कुटुंबातील सदस्यांसाठी उपयुक्त ठरू शकणाऱ्या योजना शोधण्यासाठी त्यांचा तपशील देखील जोडू शकता. भविष्यात, आपल्या परवानगीने, ओळख पडताळणी आणि अर्ज भरणे सोपे करण्यासाठी आम्ही **आधार किंवा डिजीलॉकर** वापरून सेवा देऊ शकतो. चॅटबॉटद्वारे प्रदान केलेली माहिती मार्गदर्शनासाठी आहे आणि ती योजनेच्या पात्रतेची किंवा मंजुरीची हमी देत ​​नाही. \"मी सहमत आहे आणि पुढे चालू ठेवा\" वर क्लिक करून, आपण अचूक माहिती देण्यास आणि आमचे \"गोपनीयता धोरण आणि नियम व अटी\" स्वीकारण्यास सहमत आहात।",
      agreeContinue: "मी सहमत आहे आणि पुढे चालू ठेवा"
    },
    language: {
      chooseLanguage: "आपली भाषा निवडा",
      prompt: "तुमच्या सोयीची भाषा निवडा",
      optionsLabel: "भाषा निवडा",
      hindi: "हिंदी",
      marathi: "मराठी",
      english: "English",
      selectedMessage: "भाषा निवडली आहे.",
      futureMessage: "भाषा निवडली आहे. पुढील टप्पा लवकरच उपलब्ध होईल."
    },
    login: {
      title: "लॉग इन करा",
      intro: "सरकारी योजनांची माहिती मिळवण्यासाठी तुमचा मोबाइल क्रमांक टाका.",
      mobileNumber: "मोबाइल क्रमांक",
      mobilePlaceholder: "10 अंकी मोबाइल क्रमांक",
      sendOtp: "ओटीपी पाठवा",
      enterOtp: "ओटीपी टाका",
      otpPlaceholder: "6 अंकी ओटीपी",
      verify: "पडताळणी करा",
      resendOtp: "ओटीपी पुन्हा पाठवा",
      terms: "पुढे जाऊन तुम्ही सेवेच्या अटी मान्य करता.",
      otpSent: "तुमच्या मोबाइल क्रमांकावर ओटीपी पाठवला आहे.",
      verified: "मोबाइल क्रमांकाची पडताळणी झाली. पुढील टप्पा लवकरच उपलब्ध होईल.",
      invalidMobile: "कृपया योग्य 10 अंकी मोबाइल क्रमांक टाका.",
      invalidOtp: "कृपया 6 अंकी ओटीपी टाका."
    },
    info: {
      title: "तुमची माहिती भरा",
      intro: "तुमच्यासाठी योग्य योजना शोधण्यासाठी तुमची माहिती द्या.",
      fullName: "पूर्ण नाव",
      fullNamePlaceholder: "तुमचे पूर्ण नाव टाका",
      email: "ईमेल",
      emailPlaceholder: "तुमचा ईमेल टाका",
      location: "ठिकाण",
      locationPlaceholder: "तुमचे शहर किंवा गाव टाका",
      phone: "मोबाइल क्रमांक",
      submit: "माहिती जमा करा",
      saved: "तुमची माहिती यशस्वीपणे जमा झाली आहे.",
      required: "कृपया सर्व माहिती भरा."
    }
  },
  en: {
    common: {
      welcome: "Welcome",
      tagline: "Your link to government schemes",
      headerNote: "Government scheme information, now in your language",
      continue: "Continue",
      listen: "Listen",
      back: "Back",
      changeLanguage: "Change language",
      trustMessage: "Simple • Safe • For you"
    },
    agreement: {
      title: "User Agreement & Consent",
      content: "Welcome to \"YojanaLink\", a platform that helps you find government schemes, benefits, subsidies, facilities, and other useful services. You can use our **chatbot** to ask questions, understand schemes, check basic eligibility, and get guidance in simple language. To provide better suggestions, we may ask for details such as your name, mobile number, age, occupation, location, education, and family information. Your mobile number may be verified through OTP. You can also add your family members' details to find schemes that may be useful for them. In the future, we may provide services using **Aadhaar or DigiLocker** for identity verification and easier form filling, with your permission. The information provided by the chatbot is for guidance and may not guarantee scheme eligibility or approval. By clicking \"I Agree & Continue\", you agree to provide correct information and accept our **Privacy Policy and Terms & Conditions**.",
      agreeContinue: "I Agree & Continue"
    },
    language: {
      chooseLanguage: "Choose your language",
      prompt: "Choose the language you are comfortable with",
      optionsLabel: "Choose a language",
      hindi: "हिंदी",
      marathi: "मराठी",
      english: "English",
      selectedMessage: "Language selected.",
      futureMessage: "Language selected. The next step will be available soon."
    },
    login: {
      title: "Log in",
      intro: "Enter your mobile number to access government scheme information.",
      mobileNumber: "Mobile number",
      mobilePlaceholder: "10-digit mobile number",
      sendOtp: "Send OTP",
      enterOtp: "Enter OTP",
      otpPlaceholder: "6-digit OTP",
      verify: "Verify",
      resendOtp: "Resend OTP",
      terms: "By continuing, you agree to the service terms.",
      otpSent: "An OTP has been sent to your mobile number.",
      verified: "Mobile number verified. The next step will be available soon.",
      invalidMobile: "Please enter a valid 10-digit mobile number.",
      invalidOtp: "Please enter a 6-digit OTP."
    },
    info: {
      title: "Enter your information",
      intro: "Tell us about yourself so we can find suitable schemes for you.",
      fullName: "Full name",
      fullNamePlaceholder: "Enter your full name",
      email: "Email",
      emailPlaceholder: "Enter your email",
      location: "Location",
      locationPlaceholder: "Enter your city or village",
      phone: "Mobile number",
      submit: "Submit information",
      saved: "Your information was submitted successfully.",
      required: "Please fill in all the information."
    }
  }
};

// Constants
const DEFAULT_LANGUAGE = "hi";
const LANGUAGE_KEY = "yojanalink_language";
const VERIFIED_PHONE_KEY = "yojanalink_verified_phone";
const PROFILE_KEY = "yojanalink_profile";
const AGREEMENT_KEY = "yojanalink_agreement_accepted";
const SUPPORTED_LANGUAGES = Object.keys(translations);

let activeLanguage = DEFAULT_LANGUAGE;

// ========================================
// TRANSLATION FUNCTIONS
// ========================================

function getTranslation(languageObj, key) {
  return key.split(".").reduce((value, part) => value && value[part], languageObj) || key;
}

function applyLanguage(language, saveSelection = true) {
  activeLanguage = SUPPORTED_LANGUAGES.includes(language) ? language : DEFAULT_LANGUAGE;
  const languageObj = translations[activeLanguage];

  document.documentElement.lang = activeLanguage;
  
  // Update text content for data-i18n attributes
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.innerHTML = getTranslation(languageObj, element.dataset.i18n);
  });
  
  // Update aria-labels
  document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
    element.setAttribute("aria-label", getTranslation(languageObj, element.dataset.i18nAria));
  });
  
  // Update placeholders
  document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
    element.placeholder = getTranslation(languageObj, element.dataset.i18nPlaceholder);
  });

  // Update language button states
  document.querySelectorAll(".language-option").forEach((button) => {
    const isSelected = button.dataset.language === activeLanguage;
    button.classList.toggle("is-selected", isSelected);
    button.setAttribute("aria-pressed", String(isSelected));
  });

  if (saveSelection) {
    localStorage.setItem(LANGUAGE_KEY, activeLanguage);
  }
}

function setupLanguageSelection() {
  document.querySelectorAll(".language-option").forEach((button) => {
    button.addEventListener("click", () => applyLanguage(button.dataset.language));
  });
}

function setupLanguageContinue() {
  const selectionMessage = document.querySelector(".language-panel .selection-message");
  const continueButton = document.querySelector(".language-panel .continue-button");
  if (selectionMessage && continueButton) {
    continueButton.addEventListener("click", () => {
      selectionMessage.textContent = getTranslation(translations[activeLanguage], "language.futureMessage");
    });
  }
}

// ========================================
// SPEECH SYNTHESIS FUNCTIONS
// ========================================

function getSpeechLanguage() {
  const languageMap = { hi: "hi-IN", mr: "mr-IN", en: "en-IN" };
  return languageMap[activeLanguage] || "en-IN";
}

function speakText(text) {
  if (!("speechSynthesis" in window)) {
    return;
  }

  window.speechSynthesis.cancel();
  const speech = new SpeechSynthesisUtterance(text);
  speech.lang = getSpeechLanguage();
  window.speechSynthesis.speak(speech);
}

function setupLanguageAudio() {
  const audioButton = document.querySelector(".language-audio-button");
  if (!audioButton) {
    return;
  }

  audioButton.addEventListener("click", () => {
    const languageNames = { hi: "हिंदी", mr: "मराठी", en: "English" };
    speakText(languageNames[activeLanguage]);
  });
}

// ========================================
// AGREEMENT PAGE SETUP
// ========================================

function setupAgreement() {
  const agreementButton = document.querySelector(".agreement-button");
  const audioButton = document.querySelector(".agreement-audio-button");
  
  if (!agreementButton) {
    return;
  }

  audioButton?.addEventListener("click", () => {
    const agreementText = document.querySelector(".agreement-content").textContent;
    speakText(agreementText);
  });

  agreementButton.addEventListener("click", () => {
    localStorage.setItem(AGREEMENT_KEY, "true");
    window.location.href = "login.html";
  });
}

// ========================================
// LOGIN PAGE SETUP
// ========================================

function setupLoginForm() {
  const loginForm = document.querySelector(".login-form");
  if (!loginForm) {
    return;
  }

  const mobileInput = document.querySelector("#mobile-number");
  const otpSection = document.querySelector(".otp-section");
  const otpInput = document.querySelector("#otp");
  const formMessage = document.querySelector(".mock-message");
  const resendOtpButton = document.querySelector(".resend-otp-button");
  const sendOtpButton = document.querySelector(".send-otp-button");
  const verifyButton = document.querySelector(".verify-button");

  // Send OTP handler
  sendOtpButton.addEventListener("click", () => {
    if (!/^\d{10}$/.test(mobileInput.value)) {
      formMessage.textContent = getTranslation(translations[activeLanguage], "login.invalidMobile");
      return;
    }
    otpSection.hidden = false;
    formMessage.textContent = getTranslation(translations[activeLanguage], "login.otpSent");
    otpInput.focus();
  });

  // Verify OTP handler
  verifyButton.addEventListener("click", () => {
    if (!/^\d{6}$/.test(otpInput.value)) {
      formMessage.textContent = getTranslation(translations[activeLanguage], "login.invalidOtp");
      return;
    }
    sessionStorage.setItem(VERIFIED_PHONE_KEY, mobileInput.value);
    window.location.href = "info.html";
  });

  // Resend OTP handler
  resendOtpButton.addEventListener("click", () => {
    formMessage.textContent = getTranslation(translations[activeLanguage], "login.otpSent");
  });

  loginForm.addEventListener("submit", (event) => event.preventDefault());
}

const INFO_PAGE_TEXT = {
  hi: {
    documentLabel: "दस्तावेज़ अपलोड करें",
    phoneInvalid: "कृपया 10 अंकों का सही मोबाइल नंबर दर्ज करें।",
    documentRequired: "कृपया दस्तावेज़ अपलोड करें।",
    documentInvalid: "केवल PDF, JPG या PNG फ़ाइल अपलोड करें।",
    uploading: "दस्तावेज़ अपलोड हो रहा है...",
    saved: "दस्तावेज़ सफलतापूर्वक अपलोड हो गया।"
  },

  mr: {
    documentLabel: "कागदपत्र अपलोड करा",
    phoneInvalid: "कृपया 10 अंकी योग्य मोबाईल नंबर टाका.",
    documentRequired: "कृपया कागदपत्र अपलोड करा.",
    documentInvalid: "फक्त PDF, JPG किंवा PNG फाईल अपलोड करा.",
    uploading: "कागदपत्र अपलोड होत आहे...",
    saved: "कागदपत्र यशस्वीरित्या अपलोड झाले."
  },

  en: {
    documentLabel: "Upload Document",
    phoneInvalid: "Please enter a valid 10-digit mobile number.",
    documentRequired: "Please upload a document.",
    documentInvalid: "Please upload only a PDF, JPG, or PNG file.",
    uploading: "Uploading document...",
    saved: "Document uploaded successfully."
  }
};



// ========================================
// INFO PAGE SETUP
// ========================================

function setupInfoForm() {
  const infoForm = document.querySelector(".info-form");

  if (!infoForm) {
    return;
  }

  const phoneInput = document.querySelector("#profile-phone");
  const documentInput = document.querySelector("#user-document");
  const documentLabel = document.querySelector('label[for="user-document"]');
  const formMessage = document.querySelector(".form-message");

  const verifiedPhone = sessionStorage.getItem(VERIFIED_PHONE_KEY) || "";

  // Uses the language selected on previous pages.
  const currentLanguage = INFO_PAGE_TEXT[activeLanguage] ? activeLanguage : "hi";
  const languageText = INFO_PAGE_TEXT[currentLanguage];

  // Update the new document label in selected language.
  if (documentLabel) {
    documentLabel.textContent = languageText.documentLabel;
  }

  let savedProfiles = JSON.parse(localStorage.getItem(PROFILE_KEY) || "{}");

  // Handle old profile format
  if (
    savedProfiles &&
    savedProfiles.phone &&
    !Array.isArray(Object.values(savedProfiles)[0])
  ) {
    savedProfiles = {
      [savedProfiles.phone]: savedProfiles
    };
  }

  const currentPhone = verifiedPhone || "";
  const savedProfile = savedProfiles[currentPhone];

  phoneInput.value = currentPhone || savedProfile?.phone || "";
  phoneInput.readOnly = Boolean(verifiedPhone);

  // Populate previously saved information
  if (savedProfile) {
    document.querySelector("#full-name").value = savedProfile.fullName || "";
    document.querySelector("#location").value = savedProfile.location || "";
  }

  // Form submission handler
  infoForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const documentFile = documentInput.files[0];
    const phone = phoneInput.value.trim();

    if (!infoForm.checkValidity()) {
      formMessage.textContent = getTranslation(
        translations[activeLanguage],
        "info.required"
      );

      infoForm.reportValidity();
      return;
    }

    if (!/^[0-9]{10}$/.test(phone)) {
      formMessage.textContent = languageText.phoneInvalid;
      phoneInput.focus();
      return;
    }

    if (!documentFile) {
      formMessage.textContent = languageText.documentRequired;
      documentInput.focus();
      return;
    }

    const allowedTypes = [
      "application/pdf",
      "image/jpeg",
      "image/png"
    ];

    if (!allowedTypes.includes(documentFile.type)) {
      formMessage.textContent = languageText.documentInvalid;
      documentInput.value = "";
      return;
    }

    formMessage.textContent = languageText.uploading;

    const profile = {
      fullName: document.querySelector("#full-name").value.trim(),
      location: document.querySelector("#location").value.trim(),
      phone: phone,

      // Saves document details locally.
      documentName: documentFile.name,
      documentType: documentFile.type
    };

    savedProfiles[profile.phone] = profile;
    localStorage.setItem(PROFILE_KEY, JSON.stringify(savedProfiles));

    setTimeout(() => {
      formMessage.textContent = languageText.saved;

      // Redirect to home/chat page after successful upload
      setTimeout(() => {
        window.location.href = "app.html";
      }, 800);
    }, 700);
  });
}

// ========================================
// INITIALIZATION
// ========================================

document.addEventListener("DOMContentLoaded", () => {
  // Apply saved language or default
  const savedLanguage = localStorage.getItem(LANGUAGE_KEY) || DEFAULT_LANGUAGE;
  applyLanguage(savedLanguage, false);
  
  // Setup page-specific features
  setupLanguageSelection();
  setupLanguageContinue();
  setupLanguageAudio();
  setupAgreement();
  setupLoginForm();
  setupInfoForm();

  console.log("YojanaLink initialized with language:", activeLanguage);
});

// ========================================
// END OF SCRIPT
// ========================================
