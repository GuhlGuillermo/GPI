import React, { useState, useEffect } from 'react';
import { apiClient } from '../../core/api';

const ChefDishDashboard = () => {
  const [dishes, setDishes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    nombre_plato: '',
    descripcion: '',
    precio_plato: '',
    categoria: 'ENTRANTE'
  });
  const [editingDishId, setEditingDishId] = useState(null);
  const [imageFile, setImageFile] = useState(null);

  const fetchDishes = async () => {
    try {
      const res = await apiClient.get('/dishes');
      setDishes(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchDishes();
  }, []);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setImageFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = new FormData();
      data.append('nombre_plato', formData.nombre_plato);
      data.append('descripcion', formData.descripcion);
      data.append('precio_plato', formData.precio_plato);
      data.append('categoria', formData.categoria);
      if (imageFile) {
        data.append('image', imageFile);
      }

      if (editingDishId) {
        await apiClient.put(`/dishes/${editingDishId}`, data, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      } else {
        await apiClient.post('/dishes', data, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
      }
      
      handleCancelEdit();
      fetchDishes();
    } catch (err) {
      console.error("Error guardando plato", err);
      alert("Error guardando plato");
    } finally {
      setLoading(false);
    }
  };

  const handleEditClick = (dish) => {
    setEditingDishId(dish.id_plato);
    setFormData({
      nombre_plato: dish.nombre_plato,
      descripcion: dish.descripcion || '',
      precio_plato: dish.precio_plato,
      categoria: dish.categoria
    });
    setImageFile(null);
  };

  const handleCancelEdit = () => {
    setEditingDishId(null);
    setFormData({ nombre_plato: '', descripcion: '', precio_plato: '', categoria: 'ENTRANTE' });
    setImageFile(null);
  };

  const handleDelete = async (id) => {
    if(!window.confirm('¿Seguro que deseas dar de baja este plato?')) return;
    try {
      await apiClient.delete(`/dishes/${id}`);
      fetchDishes();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="max-w-6xl mx-auto py-10 px-4">
      <h1 className="text-4xl font-black mb-8 text-slate-800">Panel del Chef - Catálogo</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* FORMULARIO */}
        <div className="bg-white p-6 inset-shadow rounded-2xl border border-slate-100 shadow-md">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">{editingDishId ? 'Editar Plato' : 'Añadir Nuevo Plato'}</h2>
            {editingDishId && <button onClick={handleCancelEdit} className="text-xs text-slate-500 hover:text-slate-800 border px-2 py-1 rounded">Cancelar</button>}
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Nombre</label>
              <input type="text" name="nombre_plato" required value={formData.nombre_plato} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-primary" />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Descripción</label>
              <textarea name="descripcion" value={formData.descripcion} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-primary" />
            </div>
            <div className="flex gap-4">
               <div className="flex-1">
                 <label className="block text-sm font-medium mb-1">Precio</label>
                 <input type="number" step="0.01" name="precio_plato" required value={formData.precio_plato} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-primary" />
               </div>
               <div className="flex-1">
                 <label className="block text-sm font-medium mb-1">Categoría</label>
                 <select name="categoria" value={formData.categoria} onChange={handleInputChange} className="w-full p-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-brand-primary bg-white">
                   <option value="ENTRANTE">Entrante</option>
                   <option value="PRINCIPAL">Principal</option>
                   <option value="POSTRE">Postre</option>
                 </select>
               </div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Imagen del Plato {editingDishId && '(Opcional para mantener actual)'}</label>
              <input type="file" accept="image/*" onChange={handleFileChange} className="w-full p-2 border border-slate-300 rounded-lg bg-slate-50 cursor-pointer" />
            </div>
            <button type="submit" disabled={loading} className="w-full bg-brand-dark text-white font-bold py-3 rounded-lg hover:bg-slate-800 transition">
              {loading ? 'Guardando...' : (editingDishId ? 'Actualizar Plato' : 'Añadir Plato al Catálogo')}
            </button>
          </form>
        </div>

        {/* LISTA */}
        <div className="col-span-1 lg:col-span-2">
          <div className="bg-white p-6 rounded-2xl border border-slate-100 shadow-md">
            <h2 className="text-xl font-bold mb-4">Platos Activos</h2>
            {dishes.length === 0 ? (
               <p className="text-slate-500">No hay platos registrados.</p>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {dishes.map(d => (
                  <div key={d.id_plato} className="flex gap-4 p-4 border border-slate-200 rounded-xl hover:border-brand-primary transition">
                    <img src={d.url_imagen || '/default-dish.png'} alt={d.nombre_plato} className="w-20 h-20 object-cover rounded-lg bg-slate-100" onError={(e) => { e.target.onerror = null; e.target.src='/default-dish.png'; }} />
                    <div className="flex-1">
                      <h4 className="font-bold flex items-center justify-between">
                         {d.nombre_plato}
                         <span className="text-sm font-normal bg-slate-100 px-2 py-0.5 rounded text-slate-600">{d.categoria}</span>
                      </h4>
                      <p className="text-xs text-slate-500 mb-2 line-clamp-1">{d.descripcion}</p>
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-brand-dark">{d.precio_plato}€</span>
                        <div className="space-x-3">
                          <button onClick={() => handleEditClick(d)} className="text-blue-500 text-sm hover:underline">Editar</button>
                          <button onClick={() => handleDelete(d.id_plato)} className="text-red-500 text-sm hover:underline">Quitar</button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChefDishDashboard;
