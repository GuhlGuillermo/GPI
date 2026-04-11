import React, { useState } from 'react';
import { apiClient } from '../../../core/api';

const ShoppingCart = ({ items, setItems }) => {
  const [cardNumber, setCardNumber] = useState('');
  
  // Estados de Red (UI Feedback State)
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  
  const subtotal = items.reduce((acc, current) => acc + (current.snapshot_price * current.quantity), 0);
  const isMinimumReached = subtotal >= 15.00;

  const handleCheckout = async (e) => {
    e.preventDefault();
    if (!isMinimumReached || cardNumber.length !== 16) return;

    setErrorMsg('');
    setSuccessMsg('');
    setLoading(true);

    try {
      // POST al adaptador Flask Blueprint 
      const response = await apiClient.post('/orders/', {
        user_id: "invitado", // Temporal (luego ID vendrá del token de autenticación)
        items: items,
        credit_card: cardNumber
      });
      
      // La API devolvió HTTP Status verde (201 OK)
      setSuccessMsg(`¡Hecho! Ticket #${response.data.order_id.substring(0,8)}. Cargado: ${response.data.total_charged.toFixed(2)}€`);
      setItems([]); // Vaciar carrito de compras porque ya se pagó con éxito
      setCardNumber('');

    } catch (err) {
      // Flask lanzó Excepciones de BusinessRuleException (HTTP 400x)
      if (err.response && err.response.data && err.response.data.error) {
        setErrorMsg(err.response.data.error);
      } else {
        // Fallos de red duros o caídas de servidor
        setErrorMsg("Los servidores del Himalaya están innacesibles en este momento.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md bg-white rounded-3xl shadow-2xl p-6 border border-slate-100 flex flex-col h-fit animate-fade-in relative overflow-hidden">
      
      {/* Superposición de Éxito de compra */}
      {successMsg && (
        <div className="absolute inset-0 z-20 bg-brand-dark flex flex-col items-center justify-center p-8 text-center animate-fade-in">
          <div className="w-20 h-20 bg-green-400 rounded-full flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(74,222,128,0.5)]">
            <svg className="w-10 h-10 text-brand-dark" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7"></path></svg>
          </div>
          <h3 className="text-2xl font-bold text-white mb-2">Pedido Recibido</h3>
          <p className="text-slate-300 font-mono text-sm">{successMsg}</p>
          <button onClick={() => setSuccessMsg('')} className="mt-8 text-brand-accent underline">Cerrar y volver</button>
        </div>
      )}

      <h2 className="text-2xl font-display font-black text-slate-800 mb-6 flex items-center gap-2">
        <span>Tu Pedido</span>
        <span className="bg-slate-100 text-slate-600 text-sm py-1 px-3 rounded-full">{items.length} items</span>
      </h2>

      {/* Listado */}
      <div className="flex-1 overflow-y-auto space-y-4 mb-6 pr-2">
        {items.map((item) => (
          <div key={item.id} className="flex justify-between items-center group">
            <div>
              <p className="font-semibold text-slate-700">{item.name}</p>
              <p className="text-sm text-slate-400">
                {item.quantity} x {item.snapshot_price.toFixed(2)}€
              </p>
            </div>
            <div className="flex items-center gap-4">
              <span className="font-bold text-slate-800">
                {(item.snapshot_price * item.quantity).toFixed(2)}€
              </span>
              <button 
                onClick={() => setItems(items.filter(i => i.id !== item.id))}
                className="text-brand-primary opacity-0 group-hover:opacity-100 transition-opacity focus:outline-none"
              >
                ✕
              </button>
            </div>
          </div>
        ))}
        {items.length === 0 && <p className="text-slate-400 text-center py-8">La cesta de manjares está vacía.</p>}
      </div>

      <div className="border-t border-slate-200 pt-4 mb-6">
        <div className="flex justify-between text-slate-600 mb-2">
          <span>Subtotal</span>
          <span>{subtotal.toFixed(2)}€</span>
        </div>
        <div className="flex justify-between text-amber-500 font-bold text-xl mt-4">
          <span>Precio de hoy</span>
          <span>{subtotal.toFixed(2)}€</span>
        </div>
      </div>

      {/* Alertajes visuales dinámicos alimentados por Backend Axios */}
      {errorMsg && (
        <div className="mb-4 bg-red-50 text-red-600 text-sm p-4 rounded-xl border border-red-200 shadow-inner flex items-start gap-3 animate-fade-in">
          <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
          <span className="font-medium">{errorMsg}</span>
        </div>
      )}

      {/* Checkout Form */}
      <form onSubmit={handleCheckout} className="space-y-4">
        <div>
          <label className="text-xs font-bold text-slate-500 uppercase tracking-widest block mb-2">Acreditación de Pago (Tarjeta)</label>
          <input 
            type="text" 
            maxLength="16"
            value={cardNumber}
            onChange={(e) => setCardNumber(e.target.value.replace(/\D/g, ''))}
            className="w-full bg-slate-50 border-2 border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:border-brand-dark transition-colors font-mono tracking-widest"
            placeholder="0000 0000 0000 0000"
            required
            disabled={loading || items.length === 0}
          />
        </div>

        {!isMinimumReached && items.length > 0 && (
          <div className="bg-slate-100 text-slate-500 text-sm p-3 rounded-xl flex justify-between items-center px-4 font-medium">
            <span>Importe mínimo: 15€</span>
            <span className="text-amber-500">- Faltan {(15 - subtotal).toFixed(2)}€</span>
          </div>
        )}

        <button 
          type="submit" 
          disabled={!isMinimumReached || cardNumber.length !== 16 || loading || items.length === 0}
          className="w-full bg-slate-900 hover:bg-slate-800 disabled:bg-slate-200 disabled:text-slate-400 text-white font-bold py-4 rounded-xl shadow-xl transition-all relative overflow-hidden"
        >
          {loading ? (
             <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5 text-white" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Procesando con Cocina...
             </span>
          ) : (
             "Confirmar Pedido & Pagar"
          )}
        </button>
      </form>
    </div>
  );
};

export default ShoppingCart;
