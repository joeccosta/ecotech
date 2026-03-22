import React, { useState } from "react";

type Props = {
  onCreate: (payload: {
    customer_name: string;
    product: string;
    quantity: number;
  }) => Promise<void>;
};

export default function OrderForm({ onCreate }: Props) {
  const [customerName, setCustomerName] = useState("");
  const [product, setProduct] = useState("");
  const [quantity, setQuantity] = useState(1);

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault();

    await onCreate({
      customer_name: customerName,
      product,
      quantity,
    });

    setCustomerName("");
    setProduct("");
    setQuantity(1);
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Criar pedido</h2>

      <div>
        <label>Cliente</label>
        <br />
        <input
          value={customerName}
          onChange={(e) => setCustomerName(e.target.value)}
          required
        />
      </div>

      <div>
        <label>Produto</label>
        <br />
        <input
          value={product}
          onChange={(e) => setProduct(e.target.value)}
          required
        />
      </div>

      <div>
        <label>Quantidade</label>
        <br />
        <input
          type="number"
          min={1}
          value={quantity}
          onChange={(e) => setQuantity(Number(e.target.value))}
          required
        />
      </div>

      <button type="submit">Criar pedido</button>
    </form>
  );
}