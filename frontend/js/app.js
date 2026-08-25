const translations = {
	hi: {
		welcome: "आपका स्वागत है",
		tagline: "आपकी योजनाओं का दुवा",
		headerNote: "सरकारी योजनाओं की जानकारी, अब आपकी भाषा में",
		chooseLanguage: "अपनी भाषा चुनें",
		languagePrompt: "अपने आराम की भाषा चुनें",
		languageOptionsLabel: "भाषा चुनें",
		hindi: "हिंदी",
		hindiEnglish: "Hindi",
		marathi: "मराठी",
		marathiEnglish: "Marathi",
		english: "English",
		englishEnglish: "English",
		continue: "आगे बढ़ें",
		listen: "सुनें",
		listenLabel: "सुनें",
		trustMessage: "सरल <span aria-hidden=\"true\">•</span> सुरक्षित <span aria-hidden=\"true\">•</span> आपके लिए",
		selectedMessage: "भाषा चुनी गई है।",
		futureMessage: "भाषा चुनी गई है। अगला चरण जल्द उपलब्ध होगा।"
	},
	mr: {
		welcome: "तुमचे स्वागत आहे",
		tagline: "तुमच्या योजनांचा दुवा",
		headerNote: "सरकारी योजनांची माहिती, आता तुमच्या भाषेत",
		chooseLanguage: "आपली भाषा निवडा",
		languagePrompt: "तुमच्या सोयीची भाषा निवडा",
		languageOptionsLabel: "भाषा निवडा",
		hindi: "हिंदी",
		hindiEnglish: "Hindi",
		marathi: "मराठी",
		marathiEnglish: "Marathi",
		english: "English",
		englishEnglish: "English",
		continue: "पुढे चला",
		listen: "ऐकून घ्या",
		listenLabel: "ऐकून घ्या",
		trustMessage: "सोपे <span aria-hidden=\"true\">•</span> सुरक्षित <span aria-hidden=\"true\">•</span> तुमच्यासाठी",
		selectedMessage: "भाषा निवडली आहे.",
		futureMessage: "भाषा निवडली आहे. पुढील टप्पा लवकरच उपलब्ध होईल."
	},
	en: {
		welcome: "Welcome",
		tagline: "Your link to government schemes",
		headerNote: "Government scheme information, now in your language",
		chooseLanguage: "Choose your language",
		languagePrompt: "Choose the language you are comfortable with",
		languageOptionsLabel: "Choose a language",
		hindi: "हिंदी",
		hindiEnglish: "Hindi",
		marathi: "मराठी",
		marathiEnglish: "Marathi",
		english: "English",
		englishEnglish: "English",
		continue: "Continue",
		listen: "Listen",
		listenLabel: "Listen",
		trustMessage: "Simple <span aria-hidden=\"true\">•</span> Safe <span aria-hidden=\"true\">•</span> For you",
		selectedMessage: "Language selected.",
		futureMessage: "Language selected. The next step will be available soon."
	}
};

const languageButtons = document.querySelectorAll(".language-option");
const continueButton = document.querySelector(".continue-button");
const selectionMessage = document.querySelector(".selection-message");
const DEFAULT_LANGUAGE = "hi";
const selectedLanguageKey = "yojanalink_language";
const supportedLanguages = Object.keys(translations);

function applyLanguage(language, saveSelection = true) {
	const currentLanguage = supportedLanguages.includes(language) ? language : DEFAULT_LANGUAGE;
	const languageText = translations[currentLanguage];

	document.documentElement.lang = currentLanguage;
	document.querySelectorAll("[data-i18n]").forEach((element) => {
		element.innerHTML = languageText[element.dataset.i18n];
	});
	document.querySelectorAll("[data-i18n-aria]").forEach((element) => {
		element.setAttribute("aria-label", languageText[element.dataset.i18nAria]);
	});

	languageButtons.forEach((button) => {
		const isSelected = button.dataset.language === currentLanguage;
		button.classList.toggle("is-selected", isSelected);
		button.setAttribute("aria-pressed", String(isSelected));
	});

	continueButton.disabled = false;
	selectionMessage.textContent = languageText.selectedMessage;
	if (saveSelection) {
		localStorage.setItem(selectedLanguageKey, currentLanguage);
	}
}

languageButtons.forEach((button) => {
	button.addEventListener("click", () => applyLanguage(button.dataset.language));
});

continueButton.addEventListener("click", () => {
	const currentLanguage = localStorage.getItem(selectedLanguageKey) || DEFAULT_LANGUAGE;
	selectionMessage.textContent = translations[currentLanguage].futureMessage;
});

const savedLanguage = localStorage.getItem(selectedLanguageKey) || DEFAULT_LANGUAGE;
applyLanguage(savedLanguage, false);

console.log("YojanaLink JavaScript loaded successfully.");
