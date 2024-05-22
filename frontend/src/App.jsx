// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'

// function App() {
//   const [input, setInput] = useState('');
//   const [response, setResponse] = useState('');

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     const res = await fetch('/api/chat', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({ input }),
//     });
//     const data = await res.json();
//     setResponse(data.response || data.message);
//   };

//   return (
//     <div>
//       <h1>Frontend con Vite</h1>
//       <form onSubmit={handleSubmit}>
//         <input
//           type="text"
//           value={input}
//           onChange={(e) => setInput(e.target.value)}
//         />
//         <button type="submit">Enviar</button>
//       </form>
//       <p>Respuesta: {response}</p>
//     </div>
//   );
// }

// export default App

import React, { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const sendMessage = async () => {
    if (input.trim() === '') return;
  
    const userMessage = { sender: 'You', text: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
  
    setInput(''); // Limpiar el texto de entrada
    setDisabled(true); // Bloquear el cuadro de texto
  
    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });
  
      const data = await response.json();
      const botMessage = { sender: 'AI', text: data.response };
      setMessages([...updatedMessages, botMessage]);
  
      setDisabled(false); // Desbloquear el cuadro de texto después de recibir la respuesta del bot
    } catch (error) {
      console.error('Error sending message:', error);
      setDisabled(false); // Asegurarse de desbloquear el cuadro de texto en caso de error
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      sendMessage();
    }
  };

  const [disabled, setDisabled] = useState(false);

  return (
    <div className="App">
      <div className="chat-container">
        <div className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <strong>{message.sender}:</strong> {message.text}
            </div>
          ))}
        </div>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={disabled} // Bloquear el cuadro de texto si está deshabilitado
        />
      </div>
    </div>
  );
}

export default App;
