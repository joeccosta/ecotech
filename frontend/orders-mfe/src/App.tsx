import "regenerator-runtime/runtime";
import React, { useEffect, useState } from "react";
import OrderForm from "./components/OrderForm";
import OrderList from "./components/OrderList";
import { createOrder, fetchOrders, Order } from "./api/orders";

export default function Root() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [statusFilter, setStatusFilter] = useState("");
  const [orderIdFilter, setOrderIdFilter] = useState("");
  const [customerNameFilter, setCustomerNameFilter] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const token = localStorage.getItem("ecotech_token");

  async function loadOrders(filters?: { status?: string; orderId?: number; customerName?: string }) {
    try {
      setLoading(true);
      setError("");
      const data = await fetchOrders(filters);
      setOrders(data.sort((a, b) => b.id - a.id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao carregar pedidos.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(payload: {
    customer_name: string;
    product: string;
    price: number;
    quantity: number;
  }) {
    try {
      setError("");
      await createOrder(payload);

      alert("Pedido criado com sucesso!");

      await loadOrders({
        status: statusFilter || undefined,
        orderId: orderIdFilter ? Number(orderIdFilter) : undefined,
        customerName: customerNameFilter || undefined,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao criar pedido.");
    }
  }

  useEffect(() => {
    if (!token) {
      window.location.href = "http://localhost:9000/login";
      return;
    }

    loadOrders({
      status: statusFilter || undefined,
      orderId: orderIdFilter ? Number(orderIdFilter) : undefined,
      customerName: customerNameFilter || undefined,
    });
  }, [token]);

  return (
    <div style={{ padding: "24px" }}>
      <h1>Ecotech Orders MFE</h1>

      <div style={{ marginBottom: "16px", display: "flex", gap: "16px", alignItems: "center", flexWrap: "wrap" }}>
        <div>
          <label htmlFor="status-filter">Filtrar por status: </label>
          <select
            id="status-filter"
            value={statusFilter}
            onChange={(e) => {
              const value = e.target.value;
              setStatusFilter(value);
              loadOrders({
                status: value || undefined,
                orderId: orderIdFilter ? Number(orderIdFilter) : undefined,
                customerName: customerNameFilter || undefined,
              });
            }}
          >
            <option value="">Todos</option>
            <option value="pending">pending</option>
            <option value="processing">processing</option>
            <option value="shipped">shipped</option>
            <option value="delivered">delivered</option>
            <option value="cancelled">cancelled</option>
          </select>
        </div>

        <div>
          <label htmlFor="order-id-filter">Filtrar por ID: </label>
          <input
            id="order-id-filter"
            type="number"
            min="1"
            value={orderIdFilter}
            onChange={(e) => {
              const value = e.target.value;
              setOrderIdFilter(value);
              loadOrders({
                status: statusFilter || undefined,
                orderId: value ? Number(value) : undefined,
                customerName: customerNameFilter || undefined,
              });
            }}
            placeholder="Ex.: 12"
          />
        </div>

        <div>
          <label htmlFor="customer-name-filter">Filtrar por cliente: </label>
          <input
            id="customer-name-filter"
            type="text"
            value={customerNameFilter}
            onChange={(e) => {
              const value = e.target.value;
              setCustomerNameFilter(value);
              loadOrders({
                status: statusFilter || undefined,
                orderId: orderIdFilter ? Number(orderIdFilter) : undefined,
                customerName: value || undefined,
              });
            }}
            placeholder="Ex.: Maria"
          />
        </div>
      </div>

      {loading && <p>Carregando pedidos...</p>}
      {error && <p>{error}</p>}

      <OrderForm onCreate={handleCreate} />
      <hr />
      <OrderList
        orders={orders}
        onStatusUpdated={() =>
          loadOrders({
            status: statusFilter || undefined,
            orderId: orderIdFilter ? Number(orderIdFilter) : undefined,
            customerName: customerNameFilter || undefined,
          })
        }
      />
    </div>
  );
}