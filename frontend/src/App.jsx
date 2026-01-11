import React, { useState, useRef, useEffect } from 'react';
import { Sparkles, Loader2, Copy, Check, Globe, Github, Send, Bot, User } from 'lucide-react';
import InitialLoader from './components/InitialLoader';
import GeneratingLoader from './components/GeneratingLoader';
import './App.css';

function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [formData, setFormData] = useState({
    purpose: 'hackathon',
    domains: [],
    tone: 'cool',
    projectDesc: '',
    customPrompt: ''
  });
  
  const [chatMessages, setChatMessages] = useState([
    {
      type: 'bot',
      content: 'Hi! I\'m Braion. Tell me about your team or project, and I\'ll create amazing names for you! 🚀'
    }
  ]);
  
  const [userInput, setUserInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const availableDomains = [
    'AI', 'IoT', 'Cybersecurity', 'Healthcare', 
    'Sustainability', 'Fintech', 'EdTech', 'Gaming',
    'Blockchain', 'Cloud Computing', 'Robotics', 'Data Science'
  ];

  // Simulate initial loading
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2500);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatMessages]);

  const toggleDomain = (domain) => {
    setFormData(prev => ({
      ...prev,
      domains: prev.domains.includes(domain)
        ? prev.domains.filter(d => d !== domain)
        : [...prev.domains, domain]
    }));
  };

  const generateNames = async (customMessage = null) => {
    setLoading(true);

    const userMessage = customMessage || userInput || 
      `Generate names for a ${formData.purpose} team in ${formData.domains.join(', ') || 'general'} domain with a ${formData.tone} tone`;
    
    setChatMessages(prev => [...prev, {
      type: 'user',
      content: userMessage
    }]);

    setUserInput('');

    // Minimum loader display time
    const minLoadingTime = new Promise(resolve => setTimeout(resolve, 1500));

    try {
      const domainsString = formData.domains.length > 0 
        ? formData.domains.join(' and ') 
        : 'general';

      const apiCall = fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          description: `${formData.purpose} team for ${domainsString}`,
          project_description: formData.projectDesc || userMessage,
          custom_prompt: formData.customPrompt || userMessage,
          tone: formData.tone,
          domain: domainsString,
          purpose: formData.purpose
        })
      });

      const [response] = await Promise.all([apiCall, minLoadingTime]);
      const data = await response.json();
      
      setChatMessages(prev => [...prev, {
        type: 'bot',
        content: 'Here are your team names! 🎯',
        meaningfulNames: data.meaningful_names || [],
        creativeNames: data.creative_names || [],
        concepts: data.concepts || []
      }]);
      
    } catch (error) {
      await minLoadingTime;
      console.error("Error:", error);
      setChatMessages(prev => [...prev, {
        type: 'bot',
        content: '❌ Oops! Could not connect to the backend. Make sure the server is running on http://127.0.0.1:8000',
        isError: true
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (userInput.trim() && !loading) {
      generateNames();
    }
  };

  const handleQuickAction = (action) => {
    switch(action) {
      case 'cool':
        setFormData(prev => ({ ...prev, tone: 'cool' }));
        generateNames('Generate cool and catchy names');
        break;
      case 'professional':
        setFormData(prev => ({ ...prev, tone: 'professional' }));
        generateNames('Generate professional and formal names');
        break;
      case 'funny':
        setFormData(prev => ({ ...prev, tone: 'funny' }));
        generateNames('Generate funny and creative names');
        break;
      case 'regenerate':
        generateNames('Generate more name options');
        break;
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
  };

  const checkAvailability = (name) => {
    const cleanName = name.toLowerCase().replace(/\s+/g, '');
    window.open(`https://www.namecheap.com/domains/registration/results/?domain=${cleanName}`, '_blank');
  };

  const checkGithub = (name) => {
    const cleanName = name.toLowerCase().replace(/\s+/g, '-');
    window.open(`https://github.com/${cleanName}`, '_blank');
  };

  // Show initial loader - THIS IS IMPORTANT
  if (isLoading) {
    return <InitialLoader />;
  }

  // Main app content - THIS MUST BE OUTSIDE THE IF STATEMENT
  return (
    <div className="app">
      <div className="container-chat">
        {/* Sidebar */}
        <div className="sidebar">
          <div className="sidebar-header">
            <div className="logo">
              <span className="logo-text">
                <span className="logo-brain">🧠</span>
                Braion
              </span>
            </div>
          </div>

          <div className="settings-section">
            <h3 className="section-title">Purpose</h3>
            <select
              value={formData.purpose}
              onChange={(e) => setFormData({...formData, purpose: e.target.value})}
              className="input"
              disabled={loading}
            >
              <option value="hackathon">Hackathon Team</option>
              <option value="startup">Startup</option>
              <option value="club">College Club</option>
              <option value="research">Research Group</option>
              <option value="competition">Competition Team</option>
            </select>
          </div>

          <div className="settings-section">
            <h3 className="section-title">Domains (Select Multiple)</h3>
            <div className="domain-chips">
              {availableDomains.map(domain => (
                <button
                  key={domain}
                  onClick={() => toggleDomain(domain)}
                  className={`chip ${formData.domains.includes(domain) ? 'chip-active' : ''}`}
                  disabled={loading}
                >
                  {domain}
                </button>
              ))}
            </div>
          </div>

          <div className="settings-section">
            <h3 className="section-title">Tone</h3>
            <select
              value={formData.tone}
              onChange={(e) => setFormData({...formData, tone: e.target.value})}
              className="input"
              disabled={loading}
            >
              <option value="professional">Professional</option>
              <option value="cool">Cool / Gen-Z</option>
              <option value="funny">Funny</option>
              <option value="aggressive">Aggressive</option>
              <option value="minimal">Minimal</option>
            </select>
          </div>

          <div className="quick-actions">
            <h3 className="section-title">Quick Actions</h3>
            <button 
              onClick={() => handleQuickAction('cool')} 
              className="quick-btn"
              disabled={loading}
            >
              😎 Cool Names
            </button>
            <button 
              onClick={() => handleQuickAction('professional')} 
              className="quick-btn"
              disabled={loading}
            >
              💼 Professional
            </button>
            <button 
              onClick={() => handleQuickAction('funny')} 
              className="quick-btn"
              disabled={loading}
            >
              😄 Funny Names
            </button>
            <button 
              onClick={() => handleQuickAction('regenerate')} 
              className="quick-btn"
              disabled={loading}
            >
              🔄 Regenerate
            </button>
          </div>
        </div>

        {/* Chat area */}
        <div className="chat-area">
          <div className="chat-header">
            <Bot className="icon" />
            <div>
              <h2 className="chat-title">Braion AI</h2>
              <p className="chat-subtitle">Your intelligent team name generator</p>
            </div>
          </div>

          <div className="chat-messages">
            {chatMessages.map((message, index) => (
              <div key={index} className={`message ${message.type}`}>
                <div className="message-icon">
                  {message.type === 'bot' ? <Bot /> : <User />}
                </div>
                <div className="message-content">
                  <p className={message.isError ? 'error-text' : ''}>{message.content}</p>
                  
                  {message.meaningfulNames && message.meaningfulNames.length > 0 && (
                    <>
                      <div className="names-category">
                        <h4 className="category-title">💡 Meaningful Names</h4>
                        <p className="category-desc">Based on your concepts and domain</p>
                      </div>
                      <div className="names-grid">
                        {message.meaningfulNames.map((name, idx) => (
                          <div key={idx} className="name-bubble">
                            <div className="name-bubble-header">
                              <span className="name-text">{name}</span>
                              <button
                                onClick={() => copyToClipboard(name)}
                                className="icon-btn-small"
                                title="Copy"
                              >
                                <Copy className="icon-tiny" />
                              </button>
                            </div>
                            <div className="name-actions">
                              <button
                                onClick={() => checkAvailability(name)}
                                className="action-link"
                              >
                                <Globe className="icon-tiny" /> Domain
                              </button>
                              <button
                                onClick={() => checkGithub(name)}
                                className="action-link"
                              >
                                <Github className="icon-tiny" /> GitHub
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </>
                  )}

                  {message.creativeNames && message.creativeNames.length > 0 && (
                    <>
                      <div className="names-category">
                        <h4 className="category-title">✨ Creative Names</h4>
                        <p className="category-desc">Cool and catchy random combinations</p>
                      </div>
                      <div className="names-grid">
                        {message.creativeNames.map((name, idx) => (
                          <div key={idx} className="name-bubble creative">
                            <div className="name-bubble-header">
                              <span className="name-text">{name}</span>
                              <button
                                onClick={() => copyToClipboard(name)}
                                className="icon-btn-small"
                                title="Copy"
                              >
                                <Copy className="icon-tiny" />
                              </button>
                            </div>
                            <div className="name-actions">
                              <button
                                onClick={() => checkAvailability(name)}
                                className="action-link"
                              >
                                <Globe className="icon-tiny" /> Domain
                              </button>
                              <button
                                onClick={() => checkGithub(name)}
                                className="action-link"
                              >
                                <Github className="icon-tiny" /> GitHub
                              </button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </>
                  )}

                  {message.concepts && (
                    <p className="concepts-text">
                      💡 Key concepts: {message.concepts.join(', ')}
                    </p>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message bot">
                <div className="message-icon">
                  <Bot />
                </div>
                <div className="message-content">
                  <GeneratingLoader />
                </div>
              </div>
            )}
            
            <div ref={chatEndRef} />
          </div>

          <form onSubmit={handleSendMessage} className="chat-input-container">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              placeholder="Describe your project or ask for specific names..."
              className="chat-input"
              disabled={loading}
            />
            <button
              type="submit"
              disabled={loading || !userInput.trim()}
              className="send-button"
            >
              <Send className="icon" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default App;