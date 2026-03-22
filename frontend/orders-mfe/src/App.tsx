import "regenerator-runtime/runtime";
import React, { useEffect, useState } from "react";
import OrderForm from "./components/OrderForm";
import OrderList from "./components/OrderList";
import { createOrder, fetchOrders, Order } from "./api/orders";

export default function Root() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function loadOrders(status?: string) {
    try {
      setLoading(true);
      setError("");
      const data = await fetchOrders(status);
      setOrders(data);
    } catch (err) {
      setError("Erro ao carregar pedidos.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(payload: {
    customer_name: string;
    product: string;
    quantity: number;
  }) {
    try {
      setError("");
      await createOrder(payload);
      await loadOrders(statusFilter || undefined);
    } catch (err) {
      setError("Erro ao criar pedido.");
    }
  }

  useEffect(() => {
    loadOrders();
  }, []);

  return (
    <div style={{ padding: "24px" }}>
      <h1>Ecotech Orders MFE</h1>

      <div style={{ marginBottom: "16px" }}>
        <label>Filtrar por status: </label>
        <select
          value={statusFilter}
          onChange={(e) => {
            const value = e.target.value;
            setStatusFilter(value);
            loadOrders(value || undefined);
          }}
        >
          <option value="">Todos</option>
          <option value="pending">pendente</option>
          <option value="processing">em processamento</option>
          <option value="completed">finalizado</option>
          <option value="cancelled">cancelado</option>
        </select>
      </div>

      {loading && <p>Carregando pedidos...</p>}
      {error && <p>{error}</p>}

      <OrderForm onCreate={handleCreate} />
      <hr />
      <OrderList orders={orders} />
    </div>
  );
}