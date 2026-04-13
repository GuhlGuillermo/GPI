import React, { useState } from 'react';
import axios from 'axios';
import { Routes, Route, Link, Navigate } from 'react-router-dom';
import ChefDishDashboard from '../admin/ChefDishDashboard';
import { apiClient } from '../../core/api';

const ChefLogin = () => {
  const [secret, setSecret] = useState('');
  const [error, setError] = useState('');
  const [token, setToken] = useState(localStorage.getItem('chef_token'));

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await apiClient.post('/auth/login', {
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
      <div className="animate-fade-in p-8 w-full max-w-6xl mx-auto mt-20">

        <div className="flex justify-between items-center bg-slate-900 border border-slate-700 p-6 rounded-2xl mb-8 shadow-2xl">
           <div>
             <h2 className="text-3xl font-display font-black text-brand-accent mb-2">Panel Maestro - Chef</h2>
             <span className="text-green-400 text-sm font-mono bg-green-400/10 px-2 py-1 rounded">✔ Sesión Verificada (JWT)</span>
           </div>
           <div className="flex gap-6 items-center">
             <Link to="/chef-admin/platos" className="text-white font-bold hover:text-brand-primary transition">🍽️ Catálogo de Platos</Link>
             <Link to="/chef-admin/menus" className="text-white font-bold hover:text-brand-primary transition">📅 Menú Diario</Link>
             <button onClick={handleLogout} className="text-slate-400 hover:text-white underline text-sm ml-4 border-l border-slate-600 pl-4">Cerrar Sesión Segura</button>
           </div>
        </div>
        
        <div className="mt-4">
            <Routes>
                <Route path="/" element={<Navigate to="platos" replace />} />
                <Route path="platos" element={
                    <div className="bg-white rounded-2xl">
                        <ChefDishDashboard />
                    </div>
                } />
                <Route path="menus" element={
                    <div className="bg-white p-16 text-center rounded-2xl border border-slate-200 mt-8 shadow-sm">
                        <h3 className="text-2xl font-bold mb-4 text-slate-800">Constructor de Menús Diarios</h3>
                        <p className="text-slate-500 max-w-md mx-auto">Selecciona qué platos de tu catálogo estarán disponibles hoy en la ruleta del cliente. (Implementación inminente)</p>
                    </div>
                } />
            </Routes>
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
