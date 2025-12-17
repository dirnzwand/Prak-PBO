# models.py
from dataclasses import dataclass
from typing import List

@dataclass
class Product:
    """Model data untuk sebuah produk."""
    id: str
    name: str
    price: float

@dataclass
class CartItem:
    """Model data untuk item di dalam keranjang belanja."""
    product: Product
    quantity: int

    @property
    def subtotal(self) -> float:
        """Menghitung subtotal untuk item ini."""
        return self.product.price * self.quantity