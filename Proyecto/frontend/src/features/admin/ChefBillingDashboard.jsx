import React, { useState, useEffect } from 'react';
import { apiClient } from '../../core/api';

const ChefBillingDashboard = () => {
  const [billingData, setBillingData] = useState({
    fecha: '---',
    total_estimado: 0.0,
    cantidad_pedidos: 0
  });
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [flushing, setFlushing] = useState(false);

  const fetchBilling = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/billing/today');
      setBillingData(res.data);
      
      const ordersRes = await apiClient.get('/orders/');
      setOrders(ordersRes.data);
    } catch (err) {
      console.error("Error obteniendo datos:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBilling();
  }, []);

  const handleFlush = async () => {
    if (!window.confirm("⚠️ ADVERTENCIA DE SEGURIDAD ⚠️\n\n¿Estás totalmente seguro de que deseas realizar el CIERRE DE CAJA? Esto volcará los datos vivos de la memoria RAM a la base de datos de MongoDB y la cuenta actual volverá a cero.\n\nSolo debes hacer esto al cerrar el restaurante.")) {
      return;
    }

    setFlushing(true);
    try {
      const res = await apiClient.post('/billing/flush');
      alert(`✅ ÉXITO:\n${res.data.message}`);
      await fetchBilling();
    } catch (err) {
      console.error("Error en cierre de caja:", err);
      alert("Hubo un error al intentar cerrar la caja. Consulta los logs técnicos.");
    } finally {
      setFlushing(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-10 px-4 animate-fade-in">
      <div className="flex justify-between items-end mb-10 border-b border-slate-200 pb-6">
        <div>
          <h1 className="text-4xl font-black text-slate-800">Métricas de Negocio</h1>
          <p className="text-slate-500 mt-2">Supervisión en tiempo real del ciclo de caja actual.</p>
        </div>
        <button 
          onClick={fetchBilling} 
          disabled={loading}
          className="bg-white border border-slate-300 text-slate-600 hover:text-brand-dark font-bold py-2 px-4 rounded-xl shadow-sm transition hover:shadow flex items-center gap-2"
        >
          {loading ? 'Sincronizando...' : '🔄 Refrescar Datos'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        {/* Card de Dinero */}
        <div className="bg-gradient-to-br from-emerald-400 to-emerald-600 rounded-3xl p-8 shadow-xl shadow-emerald-500/20 text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 p-6 opacity-20 text-6xl">💶</div>
          <h3 className="text-emerald-100 font-bold text-lg mb-2">Caja Estimada ({billingData.fecha})</h3>
          <div className="text-6xl font-black font-display tracking-tight">
             {billingData.total_estimado.toFixed(2)}<span className="text-4xl">€</span>
          </div>
          <p className="mt-4 text-emerald-100 text-sm">Recaudación combinada.</p>
        </div>

        {/* Card de Volumen */}
        <div className="bg-gradient-to-br from-indigo-500 to-indigo-700 rounded-3xl p-8 shadow-xl shadow-indigo-500/20 text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 p-6 opacity-20 text-6xl">📦</div>
          <h3 className="text-indigo-200 font-bold text-lg mb-2">Volumen de Pedidos</h3>
          <div className="text-6xl font-black font-display tracking-tight">
             {billingData.cantidad_pedidos} <span className="text-3xl font-bold opacity-75">tickets</span>
          </div>
          <p className="mt-4 text-indigo-200 text-sm">Transacciones procesadas en el turno actual.</p>
        </div>
      </div>

      <div className="bg-rose-50 border border-rose-200 rounded-2xl p-8 text-center shadow-inner">
        <h3 className="text-xl font-bold text-rose-900 mb-2">Gestión Crítica</h3>
        <p className="text-rose-700 mb-6 max-w-lg mx-auto">El cierre de caja fuerza al servidor a volcar de manera segura todos los registros temporales alojados en memoria hacia la base de datos permanente.</p>
        
        <button 
          onClick={handleFlush}
          disabled={flushing}
          className="bg-rose-600 hover:bg-rose-700 text-white text-lg font-black py-4 px-10 rounded-xl shadow-lg shadow-rose-600/30 transition-all hover:scale-105 active:scale-95 flex mx-auto items-center gap-3 disabled:opacity-50 disabled:pointer-events-none"
        >
          {flushing ? 'Procesando Volcado...' : '🔒 Ejecutar Cierre de Caja'}
        </button>
      </div>

      {/* Listado de Pedidos */}
      <div className="mt-12">
        <h2 className="text-2xl font-black text-slate-800 mb-6">Listado de Pedidos en Tiempo Real</h2>
        <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-50 text-slate-500 text-sm uppercase tracking-wider">
                  <th className="p-4 font-bold border-b border-slate-200">ID Pedido</th>
                  <th className="p-4 font-bold border-b border-slate-200">Usuario</th>
                  <th className="p-4 font-bold border-b border-slate-200">Importe</th>
                  <th className="p-4 font-bold border-b border-slate-200">Estado</th>
                  <th className="p-4 font-bold border-b border-slate-200">Hora</th>
                  <th className="p-4 font-bold border-b border-slate-200">Info Pago</th>
                  <th className="p-4 font-bold border-b border-slate-200">Origen Dato</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {orders.length > 0 ? (
                  orders.map(order => (
                    <tr key={order.id_pedido} className="hover:bg-slate-50 transition-colors">
                      <td className="p-4 text-sm font-mono text-slate-600 truncate max-w-[120px]" title={order.id_pedido}>
                        {order.id_pedido}
                      </td>
                      <td className="p-4 text-sm text-slate-700 font-medium">
                        {order.id_usuario === 'invitado' ? 'Invitado' : order.id_usuario.substring(0, 8) + '...'}
                      </td>
                      <td className="p-4 text-sm font-bold text-emerald-600">
                        {order.importe_total.toFixed(2)}€
                      </td>
                      <td className="p-4 text-sm">
                        <span className="bg-brand-light text-brand-dark px-2 py-1 rounded-md text-xs font-bold">
                          {order.estado}
                        </span>
                      </td>
                      <td className="p-4 text-sm text-slate-500">
                        {order.hora_entrega ? new Date(order.hora_entrega).toLocaleTimeString() : '---'}
                      </td>
                      <td className="p-4 text-sm text-slate-600">
                        {order.info_pago || '---'}
                      </td>
                      <td className="p-4 text-sm font-mono text-indigo-600 font-semibold bg-indigo-50">
                        {order.origen_dato}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="7" className="p-8 text-center text-slate-400">
                      No hay pedidos registrados en el sistema.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChefBillingDashboard;
