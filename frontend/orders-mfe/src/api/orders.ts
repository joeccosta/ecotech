export type Order = {
  id: number;
  customer_name: string;
  product: string;
  price: number;
  quantity: number;
  status: string;
  created_at: string;
};
/* permite o deploy em ambientes distintos, revogado */
const BASE_URL = "http://localhost:8002/orders";

const TOKEN_KEY = "ecotech_token";

function getAuthHeaders(contentType: string = "application/json") {
  const token = localStorage.getItem(TOKEN_KEY);

  return {
    "Content-Type": contentType,
    accept: "application/json",
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
}

export async function fetchOrders(status?: string): Promise<Order[]> {
  const url = status ? `${BASE_URL}/?status=${status}` : `${BASE_URL}/`;
  const response = await fetch(url, {
    headers: getAuthHeaders(),
  });

  /* explicitamente trazendo o erro */
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail) || "Erro ao buscar pedidos";
  }

  return response.json();
}

export async function createOrder(payload: {
  customer_name: string;
  product: string;
  price: number;
  quantity: number;
}): Promise<Order> {
  const response = await fetch(`${BASE_URL}/`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail) || "Falha ao criar pedido!";
  }

  return response.json();
}

export async function updateOrderStatus(id: number, status: string) {
  const response = await fetch(`${BASE_URL}/${id}/status`, {
    method: "PATCH",
    headers: getAuthHeaders(),
    body: JSON.stringify({ status }),
  });

  if (!response.ok) {
    throw new Error("Erro ao atualizar status do pedido");
  }

  return response.json();
}
