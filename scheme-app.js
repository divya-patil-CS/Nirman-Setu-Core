/* ========================================
   YOJANALINK - GOVERNMENT SCHEMES APP
   JavaScript - All Functionality
   ======================================== */

// ========================================
// DATA - Government Schemes Database
// ========================================

const governmentSchemes = [
    {
    id: 1,
    title: 'PM किसान सम्मान निधि',
    description: 'किसानों को सालाना 6000 रुपये की आर्थिक सहायता',
    badge: 'NEW',
    category: 'कृषि',
    tags: ['किसान', 'आय'],
    eligibility: 'सभी किसान',
    about: 'यह योजना छोटे और सीमांत किसानों को सालाना ₹6000 की आर्थिक सहायता प्रदान करती है।',
    benefits: [
      '₹6000 सालाना सहायता',
      'तीन किश्तों में मिलती है',
      'सभी भूमि धारक किसान पात्र'
    ],
    documents: ['आधार कार्ड', 'भूमि के दस्तावेज', 'बैंक खाता विवरण'],
    process: '1. आधिकारिक वेबसाइट पर जाएं\n2. आवश्यक जानकारी भरें\n3. दस्तावेज अपलोड करें\n4. आवेदन सबमिट करें',
    website: 'www.pmkisan.gov.in'
  },
  {
    id: 2,
    title: 'आयुष्मान भारत योजना',
    description: '5 लाख रुपये तक की स्वास्थ्य बीमा कवरेज',
    badge: 'NEW',
    category: 'स्वास्थ्य',
    tags: ['स्वास्थ्य', 'बीमा'],
    eligibility: 'निचली आय वर्ग के परिवार',
    about: 'आयुष्मान भारत योजना भारत के गरीब परिवारों को ₹5 लाख तक की स्वास्थ्य बीमा सुविधा प्रदान करती है।',
    benefits: [
      '₹5 लाख तक की बीमा कवरेज',
      '700+ निजी अस्पताल में इलाज',
      'कैशलेस उपचार'
    ],
    documents: ['राशन कार्ड', 'आधार कार्ड', 'मोबाइल नंबर'],
    process: '1. पात्रता जांचें\n2. नजदीकी आरोग्य मित्र से संपर्क करें\n3. दस्तावेज सत्यापित करें\n4. प्राप्ति पत्र लें',
    website: 'www.pmjay.gov.in'
  },
  {
    id: 3,
    title: 'स्कूल स्कॉलरशिप योजना',
    description: 'माध्यमिक छात्रों के लिए 12,000 रुपये तक छात्रवृत्ति',
    badge: 'NEW',
    category: 'शिक्षा',
    tags: ['छात्र', 'शिक्षा'],
    eligibility: '9वीं से 12वीं तक की छात्राएं',
    about: 'यह योजना गरीब और मेधावी छात्रों को शिक्षा जारी रखने के लिए वित्तीय सहायता प्रदान करती है।',
    benefits: [
      '₹12,000 सालाना छात्रवृत्ति',
      'किताब और ड्रेस के लिए अतिरिक्त राशि',
      'परीक्षा शुल्क में छूट'
    ],
    documents: ['स्कूल प्रमाण पत्र', 'आधार कार्ड', 'आय प्रमाण पत्र'],
    process: '1. स्कूल में आवेदन करें\n2. आवश्यक दस्तावेज जमा करें\n3. मेरिट के आधार पर चयन\n4. खाते में सहायता की जमा',
    website: 'www.scholarships.gov.in'
  },
  {
    id: 4,
    title: 'प्रधानमंत्री आवास योजना',
    description: 'गरीब लोगों के लिए सस्ते घर',
    badge: null,
    category: 'आवास',
    tags: ['मकान', 'आवास'],
    eligibility: 'EWS और LIG श्रेणी के परिवार',
    about: 'यह योजना गरीब और निम्न आय वर्ग के परिवारों को किफायती मूल्य पर आवास प्रदान करती है।',
    benefits: [
      'सब्सिडी वाली कीमत पर मकान',
      'आसान ऋण की सुविधा',
      'भूमि का आवंटन'
    ],
    documents: ['आधार कार्ड', 'आय प्रमाण पत्र', 'जाति प्रमाण पत्र'],
    process: '1. आवेदन पत्र भरें\n2. नोडल एजेंसी में जमा करें\n3. मेरिट सूची की प्रतीक्षा करें\n4. मकान का आवंटन',
    website: 'www.pmay.gov.in'
  },
  {
    id: 5,
    title: 'कौशल विकास योजना',
    description: 'निःशुल्क कौशल प्रशिक्षण और प्रमाणपत्र',
    badge: 'NEW',
    category: 'कौशल',
    tags: ['प्रशिक्षण', 'रोजगार'],
    eligibility: '10वीं पास के बाद के सभी युवा',
    about: 'यह योजना युवाओं को विभिन्न कौशल में निःशुल्क प्रशिक्षण प्रदान करती है।',
    benefits: [
      'निःशुल्क प्रशिक्षण',
      'अंतरराष्ट्रीय प्रमाणपत्र',
      'नौकरी सहायता'
    ],
    documents: ['10वीं पास प्रमाण पत्र', 'आधार कार्ड', 'बैंक खाता'],
    process: '1. प्रशिक्षण केंद्र चुनें\n2. ऑनलाइन पंजीकरण करें\n3. प्रशिक्षण शुरू करें\n4. परीक्षा पास करें',
    website: 'www.skillindia.gov.in'
  },
  {
    id: 6,
    title: 'मुद्रा ऋण योजना',
    description: 'छोटे व्यवसाय के लिए 10 लाख तक ऋण',
    badge: null,
    category: 'व्यवसाय',
    tags: ['ऋण', 'व्यवसाय'],
    eligibility: 'सभी नए व्यवसायी',
    about: 'MUDRA योजना छोटे व्यवसायियों को बिना गिरवी के ऋण प्रदान करती है।',
    benefits: [
      '10 लाख तक का ऋण',
      'कम ब्याज दर',
      'आसान अनुमोदन प्रक्रिया'
    ],
    documents: ['आधार कार्ड', 'व्यवसाय योजना', 'बैंक खाता'],
    process: '1. बैंक से संपर्क करें\n2. आवेदन भरें\n3. दस्तावेज जमा करें\n4. अनुमोदन के लिए प्रतीक्षा करें',
    website: 'www.mudra.org.in'
  },
  {
    id: 7,
    title: 'बेरोजगारी भत्ता',
    description: 'बेरोजगार युवाओं को मासिक भत्ता',
    badge: 'NEW',
    category: 'बेरोजगारी',
    tags: ['नौकरी', 'आय'],
    eligibility: '18-35 साल के बेरोजगार',
    about: 'यह योजना बेरोजगार युवाओं को आर्थिक सहायता और रोजगार प्रशिक्षण प्रदान करती है।',
    benefits: [
      'मासिक आर्थिक सहायता',
      'रोजगार प्रशिक्षण',
      'नौकरी खोज सहायता'
    ],
    documents: ['आधार कार्ड', 'शैक्षणिक प्रमाण पत्र', 'बेरोजगारी पंजीकरण'],
    process: '1. रोजगार कार्यालय में पंजीकरण करें\n2. आवेदन जमा करें\n3. आवेदन के लिए प्रतीक्षा करें\n4. सहायता प्राप्त करें',
    website: 'www.employment.gov.in'
  },
  {
    id: 8,
    title: 'वृद्धा पेंशन योजना',
    description: '60+ वर्षीय वरिष्ठ नागरिकों के लिए पेंशन',
    badge: null,
    category: 'सामाजिक सुरक्षा',
    tags: ['वरिष्ठ', 'पेंशन'],
    eligibility: '60 वर्ष से अधिक आयु वाले',
    about: 'यह योजना वरिष्ठ नागरिकों को सामाजिक सुरक्षा और आर्थिक सहायता प्रदान करती है।',
    benefits: [
      '500-1500 रुपये मासिक पेंशन',
      'स्वास्थ्य सुविधाएं',
      'आवास सहायता'
    ],
    documents: ['आधार कार्ड', 'आयु प्रमाण पत्र', 'आय प्रमाण पत्र'],
    process: '1. स्थानीय कार्यालय में आवेदन करें\n2. दस्तावेज सत्यापित करें\n3. अनुमोदन के लिए प्रतीक्षा करें\n4. पेंशन प्राप्त करें',
    website: 'www.socialsecurity.gov.in'
  }

];

// ========================================
// USER PROFILE DATA
// ========================================

const userProfile = {
  name: 'krushna',
  phone: '0000000000',
  education: 'BE',
  state: 'maharashtra',
  district: 'jalgaon',
  category: 'obc',
  skills: 'software engineer'
};

// ========================================
// APPLICATION STATE
// ========================================

const appState = {
  currentView: 'home',
  darkMode: localStorage.getItem('darkMode') === 'true' || false,
  fontSize: localStorage.getItem('fontSize') || 'medium',
  language: localStorage.getItem('language') || 'hi',
  notifications: true,
  otpTimer: null,
  otpTime: 30
};

// ========================================
// DOM ELEMENTS
// ========================================

const elements = {
  // Navigation
  navItems: document.querySelectorAll('.nav-item'),
  schemesList: document.getElementById('schemesList'),
  suggestionsSection: document.getElementById('suggestionsSection'),
  profileSection: document.getElementById('profileSection'),
  
  // Header Icons
  notificationBtn: document.getElementById('notificationBtn'),
  settingsBtn: document.getElementById('settingsBtn'),
  profileBtn: document.getElementById('profileBtn'),
  
  // Panels
  notificationPanel: document.getElementById('notificationPanel'),
  settingsPanel: document.getElementById('settingsPanel'),
  
  // Chatbot
  chatbotFab: document.getElementById('chatbotFab'),
  chatbotPanel: document.getElementById('chatbotPanel'),
  chatbotCloseBtn: document.getElementById('chatbotCloseBtn'),
  chatbotMessages: document.getElementById('chatbotMessages'),
  chatbotInput: document.getElementById('chatbotInput'),
  chatbotSendBtn: document.getElementById('chatbotSendBtn'),
  
  // Search
  schemeSearch: document.getElementById('schemeSearch'),
  
  // Modals
  schemeModal: document.getElementById('schemeModal'),
  profileModal: document.getElementById('profileModal'),
  modalCloseBtn: document.getElementById('modalCloseBtn'),
  profileModalCloseBtn: document.getElementById('profileModalCloseBtn'),
  modalCancelBtn: document.getElementById('modalCancelBtn'),
  applyNowBtn: document.getElementById('applyNowBtn'),
  
  // Settings
  darkModeToggle: document.getElementById('darkModeToggle'),
  notificationsToggle: document.getElementById('notificationsToggle'),
  fontSizeSelect: document.getElementById('fontSizeSelect'),
  languageSelect: document.getElementById('languageSelect'),
  
  // Profile
  editProfileBtn: document.getElementById('editProfileBtn'),
  profileForm: document.getElementById('profileForm'),
  
  // OTP
  otpTimer: document.getElementById('otpTimer'),
  verifyOtpBtn: document.getElementById('verifyOtpBtn'),
  resendOtpBtn: document.getElementById('resendOtpBtn'),
  countdownDisplay: document.getElementById('countdownDisplay')
};

// ========================================
// CHATBOT RESPONSES
// ========================================

const chatbotResponses = {
  'student': 'छात्रों के लिए हमारे पास कई योजनाएं हैं जैसे स्कूल स्कॉलरशिप, कौशल विकास योजना और शिक्षा ऋण। कौन सी योजना आपको चाहिए?',
  'scholarship': 'आप इन योजनाओं के लिए आवेदन कर सकते हैं: स्कूल स्कॉलरशिप योजना, उच्च शिक्षा छात्रवृत्ति। अधिक जानकारी के लिए योजना विवरण देखें।',
  'loan': 'व्यवसाय ऋण के लिए MUDRA योजना देखें। यह 10 लाख तक का ऋण प्रदान करती है।',
  'job': 'कौशल विकास योजना से प्रशिक्षण लें और नौकरी खोजें। हमारे पास बेरोजगारी भत्ता भी है।',
  'business': 'MUDRA योजना आपके व्यवसाय के लिए बेहतरीन है। यह बिना गिरवी के ऋण देती है।',
  'health': 'आयुष्मान भारत योजना आपको 5 लाख तक की स्वास्थ्य बीमा कवरेज देती है।',
  'house': 'प्रधानमंत्री आवास योजना गरीब परिवारों के लिए सस्ते घर प्रदान करती है।',
  'farmer': 'PM किसान सम्मान निधि योजना किसानों को सालाना 6000 रुपये देती है।',
  'pension': 'वृद्धा पेंशन योजना 60+ वर्षीय लोगों के लिए मासिक पेंशन प्रदान करती है।'
};

// ========================================
// PERSONALIZED SUGGESTIONS
// ========================================

function getPersonalizedSuggestions() {
  const userEducation = userProfile.education.toLowerCase();
  const suggestions = [];
  
  if (userEducation.includes('स्नातक') || userEducation.includes('b.sc')) {
    suggestions.push(
      governmentSchemes[4], // Skill Development
      governmentSchemes[2], // Scholarship
      governmentSchemes[5]  // MUDRA Loan
    );
  } else {
    suggestions.push(
      governmentSchemes[0], // PM Kisan
      governmentSchemes[1], // Ayushman
      governmentSchemes[3]  // Housing
    );
  }
  
  return suggestions.slice(0, 5);
}

// ========================================
// RENDER FUNCTIONS
// ========================================

function renderSchemeCards(schemesToRender = governmentSchemes) {
  const container = elements.schemesList;
  
  if (schemesToRender.length === 0) {
    container.innerHTML = `
      <div class="no-results">
        <div class="no-results-icon">🔍</div>
        <h3>कोई योजना नहीं मिली</h3>
        <p>कृपया अपनी खोज शर्तें बदलें</p>
      </div>
    `;
    return;
  }
  
  container.innerHTML = schemesToRender.map(scheme => `
    <div class="scheme-card" data-scheme-id="${scheme.id}">
      <div class="scheme-header">
        <h3 class="scheme-title">${scheme.title}</h3>
        ${scheme.badge ? `<span class="scheme-badge">${scheme.badge}</span>` : ''}
      </div>
      <p class="scheme-description">${scheme.description}</p>
      <div class="scheme-footer">
        <div>
          <span class="scheme-tag">${scheme.category}</span>
        </div>
        <span class="scheme-arrow">→</span>
      </div>
    </div>
  `).join('');
  
  // Add click handlers to scheme cards
  container.querySelectorAll('.scheme-card').forEach(card => {
    card.addEventListener('click', () => {
      const schemeId = parseInt(card.dataset.schemeId);
      const scheme = governmentSchemes.find(s => s.id === schemeId);
      if (scheme) showSchemeDetails(scheme);
    });
  });
}

function renderSuggestions() {
  const suggestions = getPersonalizedSuggestions();
  const container = document.getElementById('suggestionsList');
  
  if (!container) return;
  
  container.innerHTML = suggestions.map(suggestion => `
    <div class="suggestion-item" data-scheme-id="${suggestion.id}">
      <div class="suggestion-info">
        <h3>${suggestion.title}</h3>
        <p>${suggestion.description}</p>
      </div>
      <span class="suggestion-match">95% मेल</span>
    </div>
  `).join('');
  
  container.querySelectorAll('.suggestion-item').forEach(item => {
    item.addEventListener('click', () => {
      const schemeId = parseInt(item.dataset.schemeId);
      const scheme = governmentSchemes.find(s => s.id === schemeId);
      if (scheme) showSchemeDetails(scheme);
    });
  });
}

function showSchemeDetails(scheme) {
  const modal = elements.schemeModal;
  const modalBody = document.getElementById('modalBody');
  
  const detailsHTML = `
    <div class="scheme-detail-group">
      <h3>${scheme.title}</h3>
      <p>${scheme.description}</p>
    </div>
    
    <div class="scheme-detail-group">
      <h3>योजना के बारे में</h3>
      <p>${scheme.about}</p>
    </div>
    
    <div class="scheme-detail-group">
      <h3>पात्रता</h3>
      <p>${scheme.eligibility}</p>
    </div>
    
    <div class="scheme-detail-group">
      <h3>लाभ</h3>
      <ul>
        ${scheme.benefits.map(benefit => `<li>${benefit}</li>`).join('')}
      </ul>
    </div>
    
    <div class="scheme-detail-group">
      <h3>आवश्यक दस्तावेज</h3>
      <ul>
        ${scheme.documents.map(doc => `<li>${doc}</li>`).join('')}
      </ul>
    </div>
    
    <div class="scheme-detail-group">
      <h3>आवेदन प्रक्रिया</h3>
      <p>${scheme.process.replace(/\n/g, '<br>')}</p>
    </div>
    
    <div class="scheme-detail-group">
      <h3>आधिकारिक वेबसाइट</h3>
      <p><a href="https://${scheme.website}" target="_blank" style="color: var(--primary-color);">${scheme.website}</a></p>
    </div>
  `;
  
  modalBody.innerHTML = detailsHTML;
  modal.classList.add('visible');
}

// ========================================
// NAVIGATION HANDLING
// ========================================

// यह फंक्शन अलग-अलग pages को दिखाता है (होम, सुझाव, प्रोफाइल)
function switchView(view) {
  // कौन सा view active है यह याद रखें
  appState.currentView = view;
  
  // पहले सभी sections को छिपा दें
  elements.schemesList.parentElement.style.display = 'none';
  elements.suggestionsSection.style.display = 'none';
  elements.profileSection.style.display = 'none';
  
  // अब जो section चुना गया है उसे दिखा दें
  switch(view) {
    case 'home':
      // होम पेज में schemes दिखाएं
      elements.schemesList.parentElement.style.display = 'block';
      break;
    case 'suggestions':
      // सुझाव पेज में personalized suggestions दिखाएं
      renderSuggestions();
      elements.suggestionsSection.style.display = 'block';
      break;
    case 'profile':
      // प्रोफाइल पेज दिखाएं
      elements.profileSection.style.display = 'block';
      break;
  }
  
  // navigation buttons को update करें (active color लगाएं)
  elements.navItems.forEach(item => {
    item.classList.remove('active');  // सभी से active class हटा दें
    if (item.dataset.nav === view) {
      item.classList.add('active');   // सही button को active बना दें
    }
  });
  
  // Scroll to top
  document.querySelector('.main-content').scrollTop = 0;
}

// ========================================
// PANEL TOGGLES
// ========================================

function togglePanel(panel) {
  // Close other panels
  if (panel !== elements.notificationPanel) {
    elements.notificationPanel.classList.remove('visible');
  }
  if (panel !== elements.settingsPanel) {
    elements.settingsPanel.classList.remove('visible');
  }
  
  // Toggle current panel
  panel.classList.toggle('visible');
}

// ========================================
// CHATBOT FUNCTIONS (चैटबॉट के फंक्शन)
// ========================================

// यह फंक्शन chatbot को खोलता और बंद करता है
function toggleChatbot() {
  // chatbot को toggle करें (hidden ↔ visible)
  elements.chatbotPanel.classList.toggle('hidden');
  
  // अगर chatbot अब दिख रहा है तो input में cursor डालें
  if (!elements.chatbotPanel.classList.contains('hidden')) {
    elements.chatbotInput.focus();
  }
}

// यह फंक्शन user के message को send करता है
function sendChatbotMessage() {
  // input field से text निकालें
  const message = elements.chatbotInput.value.trim();
  
  // अगर message खाली है तो कुछ मत करो
  if (!message) return;
  
  // user का message chatbot के screen पर दिखाएं
  addChatMessage(message, 'user');
  elements.chatbotInput.value = '';
  
  // Simulate bot typing
  setTimeout(() => {
    const response = getChatbotResponse(message);
    addChatMessage(response, 'bot');
  }, 500);
}

function addChatMessage(text, sender) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `chat-message ${sender}-message`;
  messageDiv.innerHTML = `<p>${text}</p>`;
  elements.chatbotMessages.appendChild(messageDiv);
  elements.chatbotMessages.scrollTop = elements.chatbotMessages.scrollHeight;
}

function getChatbotResponse(userMessage) {
  const lowerMessage = userMessage.toLowerCase();
  
  // Check for keywords
  for (const [keyword, response] of Object.entries(chatbotResponses)) {
    if (lowerMessage.includes(keyword)) {
      return response;
    }
  }
  
  // Default response
  return 'कृपया अपने प्रश्न को विस्तार से समझाएं। हम आपकी सहायता के लिए यहां हैं। 🤝';
}

// ========================================
// OTP TIMER FUNCTIONS
// ========================================

function startOtpTimer() {
  elements.otpTimer.style.display = 'block';
  appState.otpTime = 30;
  elements.resendOtpBtn.disabled = true;
  
  const timerInterval = setInterval(() => {
    appState.otpTime--;
    const minutes = Math.floor(appState.otpTime / 60);
    const seconds = appState.otpTime % 60;
    elements.countdownDisplay.textContent = 
      `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    
    if (appState.otpTime <= 0) {
      clearInterval(timerInterval);
      elements.resendOtpBtn.disabled = false;
      addChatMessage('OTP की समय सीमा समाप्त हो गई। कृपया फिर से OTP मांगें।', 'bot');
    }
  }, 1000);
  
  appState.otpTimer = timerInterval;
}

function resendOtp() {
  addChatMessage('नया OTP आपके मोबाइल नंबर पर भेज दिया गया है।', 'bot');
  startOtpTimer();
}

// ========================================
// SEARCH FUNCTIONALITY (योजना खोजना)
// ========================================

// यह फंक्शन schemes को खोजता है जब user search box में कुछ टाइप करे
function searchSchemes(query) {
  // search text को छोटे letters में बदल दें (ताकि match करना आसान हो)
  const lowerQuery = query.toLowerCase();
  
  // schemes के array से सिर्फ वो schemes निकालें जो query से match करें
  const filtered = governmentSchemes.filter(scheme => 
    // Scheme का title match करे? या
    scheme.title.toLowerCase().includes(lowerQuery) ||
    // Scheme का description match करे? या
    scheme.description.toLowerCase().includes(lowerQuery) ||
    // Scheme का category match करे? या
    scheme.category.toLowerCase().includes(lowerQuery) ||
    // Scheme के tags में से कोई match करे?
    scheme.tags.some(tag => tag.toLowerCase().includes(lowerQuery))
  );
  
  // अब सिर्फ match करने वाली schemes को दिखाएं
  renderSchemeCards(filtered);
}

// ========================================
// DARK MODE FUNCTIONALITY (रात का मोड)
// ========================================

// यह फंक्शन रात के मोड को ON/OFF करता है
function toggleDarkMode() {
  // dark mode को toggle करें (ON → OFF, OFF → ON)
  appState.darkMode = !appState.darkMode;
  
  // CSS class को add/remove करें (यह visual look बदल देता है)
  document.body.classList.toggle('dark-mode');
  
  // setting को browser की मेमोरी में save करें
  localStorage.setItem('darkMode', appState.darkMode);
}

// ========================================
// FONT SIZE FUNCTIONALITY (फॉन्ट साइज बदलना)
// ========================================

// यह फंक्शन फॉन्ट साइज को छोटा, मध्यम या बड़ा करता है
function changeFontSize(size) {
  // सबसे पहले पुरानी क्लास हटा दें
  document.body.classList.remove('font-small', 'font-large');
  
  // अगर साइज medium नहीं है तो नई क्लास लगा दें
  if (size !== 'medium') {
    document.body.classList.add(`font-${size}`);
  }
  
  // साइज को app state में सेव करें
  appState.fontSize = size;
  
  // साइज को browser की मेमोरी में सेव करें (ताकि अगली बार खुलने पर याद रहे)
  localStorage.setItem('fontSize', size);
}

// ========================================
// LANGUAGE FUNCTIONALITY (भाषा बदलना)
// ========================================

// यह फंक्शन एप्लिकेशन की भाषा को हिंदी, मराठी या अंग्रेजी में बदलता है
function changeLanguage(lang) {
  // भाषा को app state में स्टोर करें (याद रखने के लिए)
  appState.language = lang;
  
  // भाषा को browser की मेमोरी में सेव करें
  localStorage.setItem('language', lang);
  
  // भाषा को user profile में भी सेव करें (ताकि अगली बार लॉगिन पर वही भाषा लाइ)
  userProfile.language = lang;
  
  // HTML का lang attribute बदलें (यह स्क्रीन रीडर्स के लिए जरूरी है)
  document.documentElement.lang = lang;
  
  // ===== भाषा के अनुसार UI टेक्स्ट बदलें =====
  
  // हर भाषा के लिए विस्तृत text का dictionary बनाएं
  const translations = {
    // हिंदी भाषा
    hi: {
      chatbotHeader: 'YojanaLink सहायता',
      navHome: 'होम',
      navSuggestions: 'सुझाव',
      navProfile: 'आईडी',
      schemeHeader: 'सरकारी योजनाएं',
      schemeSubtitle: 'आपके लिए उपलब्ध सरकारी योजनाएं',
      searchPlaceholder: 'योजना खोजें...',
      suggestionsHeader: 'आपके लिए सुझाव',
      suggestionsSubtitle: 'आपकी जानकारी के आधार पर अनुशंसित योजनाएं',
      profileHeader: 'आपकी प्रोफाइल',
      profileSubtitle: 'अपनी जानकारी देखें और संपादित करें',
      applyNow: 'अभी आवेदन करें',
      editProfile: 'प्रोफाइल संपादित करें',
      updateProfile: 'अपडेट करें',
      signOut: 'साइन आउट'
    },
    // मराठी भाषा
    mr: {
      chatbotHeader: 'YojanaLink समर्थन',
      navHome: 'होम',
      navSuggestions: 'सुझाव',
      navProfile: 'आईडी',
      schemeHeader: 'सरकारी योजना',
      schemeSubtitle: 'तुमच्यासाठी उपलब्ध सरकारी योजना',
      searchPlaceholder: 'योजना शोधा...',
      suggestionsHeader: 'तुमच्यासाठी सुझाव',
      suggestionsSubtitle: 'तुमच्या माहितीच्या आधारावर शिफारस केलेल्या योजना',
      profileHeader: 'तुमची प्रोफाइल',
      profileSubtitle: 'तुमची माहिती पहा आणि संपादित करा',
      applyNow: 'आता अर्ज करा',
      editProfile: 'प्रोफाइल संपादित करा',
      updateProfile: 'अपडेट करा',
      signOut: 'साइन आउट'
    },
    // अंग्रेजी भाषा
    en: {
      chatbotHeader: 'YojanaLink Support',
      navHome: 'Home',
      navSuggestions: 'Suggestions',
      navProfile: 'Profile',
      schemeHeader: 'Government Schemes',
      schemeSubtitle: 'Government schemes available for you',
      searchPlaceholder: 'Search schemes...',
      suggestionsHeader: 'Suggestions for you',
      suggestionsSubtitle: 'Recommended schemes based on your information',
      profileHeader: 'Your Profile',
      profileSubtitle: 'View and edit your information',
      applyNow: 'Apply Now',
      editProfile: 'Edit Profile',
      updateProfile: 'Update',
      signOut: 'Sign Out'
    }
  };
  
  // अगर भाषा गलत हो तो हिंदी डिफॉल्ट करें
  const t = translations[lang] || translations.hi;
  
  // ===== अब page के सभी elements को नई भाषा में बदलें =====
  
  // 1. Chatbot का header बदलें
  const chatbotHeader = document.querySelector('.chatbot-header h3');
  if (chatbotHeader) {
    chatbotHeader.textContent = t.chatbotHeader;
  }
  
  // 2. नीचे की navigation (होम, सुझाव, आईडी) को बदलें
  const navItems = document.querySelectorAll('.nav-item span');
  if (navItems.length >= 3) {
    navItems[0].textContent = t.navHome;           // पहला बटन = होम
    navItems[1].textContent = t.navSuggestions;    // दूसरा बटन = सुझाव
    navItems[2].textContent = t.navProfile;        // तीसरा बटन = आईडी
  }
  
  // 3. scheme सेक्शन का heading बदलें
  const schemeHeader = document.querySelector('.schemes-header h2');
  if (schemeHeader) {
    schemeHeader.textContent = t.schemeHeader;
  }
  
  // 4. scheme सेक्शन का subtitle बदलें
  const schemeSubtitle = document.querySelector('.schemes-subtitle');
  if (schemeSubtitle) {
    schemeSubtitle.textContent = t.schemeSubtitle;
  }
  
  // 5. search input का placeholder बदलें
  const searchInput = document.querySelector('.search-input');
  if (searchInput) {
    searchInput.placeholder = t.searchPlaceholder;
  }
  
  // 6. Suggestions section का header बदलें
  const suggestionsHeader = document.querySelector('.suggestions-section .section-header h2');
  if (suggestionsHeader) {
    suggestionsHeader.textContent = t.suggestionsHeader;
  }
  
  // 7. Suggestions section का subtitle बदलें
  const suggestionsSubtitle = document.querySelector('.suggestions-section .section-subtitle');
  if (suggestionsSubtitle) {
    suggestionsSubtitle.textContent = t.suggestionsSubtitle;
  }
  
  // 8. Profile section का header बदलें
  const profileHeader = document.querySelector('.profile-section .profile-header h2');
  if (profileHeader) {
    profileHeader.textContent = t.profileHeader;
  }
  
  // 9. Profile section का subtitle बदलें
  const profileSubtitle = document.querySelector('.profile-section .section-subtitle');
  if (profileSubtitle) {
    profileSubtitle.textContent = t.profileSubtitle;
  }
  
  // 10. Edit Profile बटन का टेक्स्ट बदलें
  const editProfileBtn = document.getElementById('editProfileBtn');
  if (editProfileBtn) {
    editProfileBtn.textContent = t.editProfile;
  }
  
  // 11. Modal headers बदलें
  const modalHeaders = document.querySelectorAll('.modal-header h2');
  modalHeaders.forEach((header) => {
    if (header.textContent.includes('योजना') || header.textContent.includes('Scheme')) {
      header.textContent = t.schemeHeader;
    }
  });
  
  // 12. Sign Out बटन का टेक्स्ट बदलें
  const signOutBtn = document.getElementById('signOutBtn');
  if (signOutBtn) {
    signOutBtn.textContent = t.signOut;
  }
}

// ========================================
// SIGN OUT FUNCTIONALITY (साइन आउट करना)
// ========================================

// यह फंक्शन user को साइन आउट करता है और सभी डेटा को साफ करता है
function signOut() {
  // User से पुष्टि मांगें कि क्या वह सच में साइन आउट करना चाहता है
  const confirmSignOut = confirm('क्या आप वाकई साइन आउट करना चाहते हैं?\n\nAre you sure you want to sign out?');
  
  // अगर user ने नहीं कहा तो वापस चला जाएं
  if (!confirmSignOut) {
    return;
  }
  
  // सभी localStorage डेटा को साफ करें (भाषा, प्रोफाइल इत्यादि)
  localStorage.clear();
  
  // सभी sessionStorage डेटा को साफ करें (verified phone number इत्यादि)
  sessionStorage.clear();
  
  // User को login page पर redirect करें
  window.location.href = 'login.html';
}

// ========================================
// PROFILE FUNCTIONS
// ========================================

function updateProfileDisplay() {
  // Profile information display has been removed from UI
  // Only the edit button is shown now
  // No elements to update here
}

function showProfileEditModal() {
  document.getElementById('editName').value = userProfile.name;
  document.getElementById('editPhone').value = userProfile.phone;
  document.getElementById('editEducation').value = userProfile.education;
  document.getElementById('editState').value = userProfile.state;
  document.getElementById('editDistrict').value = userProfile.district;
  document.getElementById('editCategory').value = userProfile.category;
  document.getElementById('editSkills').value = userProfile.skills;
  
  elements.profileModal.classList.add('visible');
}

function saveProfileChanges(e) {
  e.preventDefault();
  
  userProfile.name = document.getElementById('editName').value;
  userProfile.phone = document.getElementById('editPhone').value;
  userProfile.education = document.getElementById('editEducation').value;
  userProfile.state = document.getElementById('editState').value;
  userProfile.district = document.getElementById('editDistrict').value;
  userProfile.category = document.getElementById('editCategory').value;
  userProfile.skills = document.getElementById('editSkills').value;
  
  updateProfileDisplay();
  elements.profileModal.classList.remove('visible');
  
  // Show success message in chatbot
  addChatMessage('आपकी प्रोफाइल सफलतापूर्वक अपडेट हो गई है! ✅', 'bot');
}

// ========================================
// EVENT LISTENERS
// ========================================

// जब पूरा page लोड हो जाए तो यह कोड चलेगा
document.addEventListener('DOMContentLoaded', () => {
  
  // ===== APP शुरु करें =====
  renderSchemeCards();        // सभी scheme cards को दिखाएं
  updateProfileDisplay();     // user का profile दिखाएं
  
  // ===== LANGUAGE को apply करें (जो पहले से सेव है) =====
  // अगर कोई भाषा पहले से चुनी गई है तो वह भाषा अब लगा दें
  if (appState.language) {
    elements.languageSelect.value = appState.language;  // dropdown में वह भाषा select करें
    changeLanguage(appState.language);                  // पूरे app की भाषा बदल दें
  }
  
  // ===== DARK MODE को apply करें (जो पहले से सेव है) =====
  if (appState.darkMode) {
    document.body.classList.add('dark-mode');       // dark mode की class लगा दें
    elements.darkModeToggle.checked = true;         // toggle button को ON करें
  }
  
  // ===== FONT SIZE को apply करें (जो पहले से सेव है) =====
  if (appState.fontSize !== 'medium') {
    document.body.classList.add(`font-${appState.fontSize}`);  // font size की class लगा दें
    elements.fontSizeSelect.value = appState.fontSize;         // dropdown में वह size select करें
  }
  
  // ========================================
  // NAVIGATION (नीचे के बटन) 
  // ========================================
  
  // हर navigation बटन पर क्लिक करने के लिए
  elements.navItems.forEach(item => {
    item.addEventListener('click', () => {
      switchView(item.dataset.nav);  // सही page दिखाएं (होम/सुझाव/प्रोफाइल)
    });
  });
  
  // ========================================
  // HEADER ICONS (ऊपर के बटन)
  // ========================================
  
  elements.notificationBtn.addEventListener('click', () => {
    togglePanel(elements.notificationPanel);
  });
  
  elements.settingsBtn.addEventListener('click', () => {
    togglePanel(elements.settingsPanel);
  });
  
  // Close panels when clicking elsewhere
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.notification-btn') && 
        !e.target.closest('.notification-panel')) {
      elements.notificationPanel.classList.remove('visible');
    }
    if (!e.target.closest('.settings-btn') && 
        !e.target.closest('.settings-panel')) {
      elements.settingsPanel.classList.remove('visible');
    }
  });
  
  // ========================================
  // SEARCH
  // ========================================
  
  elements.schemeSearch.addEventListener('input', (e) => {
    searchSchemes(e.target.value);
  });
  
  // ========================================
  // CHATBOT
  // ========================================
  
  elements.chatbotFab.addEventListener('click', toggleChatbot);
  elements.chatbotCloseBtn.addEventListener('click', toggleChatbot);
  
  elements.chatbotSendBtn.addEventListener('click', sendChatbotMessage);
  elements.chatbotInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendChatbotMessage();
  });
  
  // ========================================
  // MODALS
  // ========================================
  
  elements.modalCloseBtn.addEventListener('click', () => {
    elements.schemeModal.classList.remove('visible');
  });
  
  elements.modalCancelBtn.addEventListener('click', () => {
    elements.schemeModal.classList.remove('visible');
  });
  
  elements.applyNowBtn.addEventListener('click', () => {
    addChatMessage('आपका आवेदन सफलतापूर्वक जमा हो गया है। शीघ्र ही आपको विस्तृत जानकारी दी जाएगी। 📧', 'bot');
    elements.schemeModal.classList.remove('visible');
    setTimeout(() => toggleChatbot(), 500);
  });
  
  elements.profileModalCloseBtn.addEventListener('click', () => {
    elements.profileModal.classList.remove('visible');
  });
  
  // Close modals when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target === elements.schemeModal) {
      elements.schemeModal.classList.remove('visible');
    }
    if (e.target === elements.profileModal) {
      elements.profileModal.classList.remove('visible');
    }
  });
  
  // ========================================
  // SETTINGS
  // ========================================
  
  elements.darkModeToggle.addEventListener('change', toggleDarkMode);
  
  // जब फॉन्ट साइज चेंज हो तो changeFontSize फंक्शन कॉल करें
  elements.fontSizeSelect.addEventListener('change', (e) => {
    changeFontSize(e.target.value);
  });
  
  // जब भाषा चेंज हो तो changeLanguage फंक्शन कॉल करें
  elements.languageSelect.addEventListener('change', (e) => {
    changeLanguage(e.target.value);
  });
  
  // नोटिफिकेशन टॉगल करने के लिए
  elements.notificationsToggle.addEventListener('change', (e) => {
    appState.notifications = e.target.checked;
  });
  
  // ========================================
  // PROFILE
  // ========================================
  
  elements.editProfileBtn.addEventListener('click', showProfileEditModal);
  elements.profileForm.addEventListener('submit', saveProfileChanges);
  
  // Close profile modal btn
  elements.profileModalCloseBtn.addEventListener('click', () => {
    elements.profileModal.classList.remove('visible');
  });
  
  // Sign Out बटन के लिए event listener जोड़ें
  const signOutBtn = document.getElementById('signOutBtn');
  if (signOutBtn) {
    signOutBtn.addEventListener('click', signOut);
  }
  
  // ========================================
  // OTP
  // ========================================
  
  elements.verifyOtpBtn.addEventListener('click', () => {
    const otp = document.getElementById('otpInput').value;
    if (otp.length === 6) {
      addChatMessage('OTP सत्यापित हो गया! 🎉', 'bot');
      elements.otpTimer.style.display = 'none';
      document.getElementById('otpInput').value = '';
    } else {
      addChatMessage('कृपया 6 अंकों का सही OTP दर्ज करें।', 'bot');
    }
  });
  
  elements.resendOtpBtn.addEventListener('click', resendOtp);
  
  // ========================================
  // RESPONSIVE BEHAVIOR
  // ========================================
  
  // Prevent panel overflow on small screens
  const updateViewportHeight = () => {
    const vh = window.innerHeight * 0.01;
    document.documentElement.style.setProperty('--vh', `${vh}px`);
  };
  
  updateViewportHeight();
  window.addEventListener('resize', updateViewportHeight);
  
  // Show welcome message in chatbot
  setTimeout(() => {
    addChatMessage('नमस्ते! मैं आपकी सरकारी योजनाएं खोजने में मदद कर सकता हूं। क्या आप जानना चाहते हैं कि कौन सी योजना आपके लिए सही है? 😊', 'bot');
  }, 1000);
});

// ========================================
// UTILITY FUNCTIONS
// ========================================

// Prevent multiple rapid clicks
function debounce(func, delay) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, delay);
  };
}

// Handle offline/online status
window.addEventListener('online', () => {
  addChatMessage('आप ऑनलाइन हैं। 🟢', 'bot');
});

window.addEventListener('offline', () => {
  addChatMessage('आप ऑफलाइन हैं। कृपया इंटरनेट कनेक्शन जांचें। 🔴', 'bot');
});

// ========================================
// END OF SCRIPT
// ========================================
