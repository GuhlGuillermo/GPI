import React, { useState } from 'react';
import axios from 'axios';

const ChefLogin = () => {
  const [secret, setSecret] = useState('');
  const [error, setError] = useState('');
  const [token, setToken] = useState(localStorage.getItem('chef_token'));

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Mocked connect to true endpoint. Si falla lo mockeamos para demo frontend.
      const response = await axios.post('http://localhost:5000/api/auth/login', {
        role: "CHEF",
        secret_key: secret
      });
      const jwt = response.data.token;
      localStorage.setItem('chef_token', jwt);
      setToken(jwt);
    } catch (err) {
      setError('Credenciales de chef inválidas. Estación denegada.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('chef_token');
    setToken(null);
  };

  if (token) {
    return (
      <div className="animate-fade-in p-8 w-full max-w-4xl mx-auto mt-20">
        <div className="flex justify-between items-center bg-slate-900 border border-slate-700 p-6 rounded-2xl mb-8 shadow-2xl">
           <div>
             <h2 className="text-3xl font-display font-black text-brand-accent mb-2">Panel Maestro - Chef</h2>
             <span className="text-green-400 text-sm font-mono bg-green-400/10 px-2 py-1 rounded">✔ Sesión Verificada (JWT)</span>
           </div>
           <button onClick={handleLogout} className="text-slate-400 hover:text-white underline text-sm">Cerrar Sesión Segura</button>
        </div>
        
        <div className="grid grid-cols-2 gap-8">
            <div className="border border-dashed border-slate-300 p-12 text-center rounded-2xl bg-white/50 text-slate-500">
                Lógica CRUD Platos (Próximo Sprint)
            </div>
            <div className="border border-dashed border-slate-300 p-12 text-center rounded-2xl bg-white/50 text-slate-500">
                Gestión Menú (Próximo Sprint)
            </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white rounded-3xl p-8 border border-slate-100 shadow-2xl">
        <div className="text-center mb-8">
            <div className="bg-rose-100 text-brand-primary w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4 rotate-3">
                <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8V7a4 4 0 00-8 0v4h8z"></path></svg>
            </div>
            <h1 className="text-3xl font-display font-black text-slate-800">Portal Privado</h1>
            <p className="text-slate-500 text-sm mt-2">Acceso restringido a empleados del restaurante.</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label className="text-xs font-bold text-slate-500 uppercase tracking-widest block mb-2">Clave Maestra de Chef</label>
            <input 
              type="password" 
              value={secret} 
              onChange={e => setSecret(e.target.value)}
              className="w-full bg-slate-50 border-2 border-slate-200 p-4 rounded-xl focus:border-brand-primary focus:ring-0 transition-colors font-mono tracking-widest text-center text-xl"
              placeholder="••••••••"
              required
            />
          </div>
          
          {error && <div className="text-red-500 text-sm font-semibold bg-red-50 p-3 rounded-lg text-center">{error}</div>}

          <button type="submit" className="w-full bg-slate-900 hover:bg-slate-800 text-white font-bold py-4 rounded-xl shadow-lg transition-colors">
            Autenticar
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChefLogin;
