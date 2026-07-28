// Master Data State
let products = [
    // 1. Atta & Flour
    { id: "PRD-001", name: "Aashirvaad Whole Wheat Atta", code: "PRD-001", category: "Atta & Flour", unit: "Kg", purchasePrice: 190, sellingPrice: 210, desc: "Premium whole wheat flour.", imgUrl: "assets/images/products/gen_atta.png", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-002", name: "Fortune Chakki Fresh Atta", code: "PRD-002", category: "Atta & Flour", unit: "Kg", purchasePrice: 380, sellingPrice: 420, desc: "100% Atta, 0% Maida.", imgUrl: "https://images.unsplash.com/photo-1608686207856-001b95cf60ca?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-003", name: "Pillsbury Gold Atta", code: "PRD-003", category: "Atta & Flour", unit: "Kg", purchasePrice: 220, sellingPrice: 240, desc: "Premium quality wheat flour.", imgUrl: "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-004", name: "Rajdhani Besan", code: "PRD-004", category: "Atta & Flour", unit: "Packet", purchasePrice: 45, sellingPrice: 55, desc: "Gram flour (Besan) 500g.", imgUrl: "https://images.unsplash.com/photo-1627485937980-221c88ab04f9?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-005", name: "Nature Fresh Maida", code: "PRD-005", category: "Atta & Flour", unit: "Kg", purchasePrice: 50, sellingPrice: 60, desc: "Refined wheat flour 1Kg.", imgUrl: "https://images.unsplash.com/photo-1587314168485-3236d6710814?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },

    // 2. Bakery
    { id: "PRD-006", name: "Britannia White Bread", code: "PRD-006", category: "Bakery", unit: "Packet", purchasePrice: 35, sellingPrice: 40, desc: "Classic white bread 400g.", imgUrl: "assets/images/products/gen_bread.png", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-007", name: "Harvest Gold Brown Bread", code: "PRD-007", category: "Bakery", unit: "Packet", purchasePrice: 40, sellingPrice: 45, desc: "Healthy brown bread 400g.", imgUrl: "https://images.unsplash.com/photo-1586444248902-2f64eddc13df?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-008", name: "English Oven Burger Buns", code: "PRD-008", category: "Bakery", unit: "Packet", purchasePrice: 30, sellingPrice: 35, desc: "Soft burger buns 4pcs.", imgUrl: "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-009", name: "Bonn Garlic Bread", code: "PRD-009", category: "Bakery", unit: "Packet", purchasePrice: 45, sellingPrice: 55, desc: "Toasted garlic bread 200g.", imgUrl: "https://images.unsplash.com/photo-1619535860434-ba1d8fa12536?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-010", name: "Wibs Sandwich Bread", code: "PRD-010", category: "Bakery", unit: "Packet", purchasePrice: 30, sellingPrice: 35, desc: "Jumbo sandwich bread 400g.", imgUrl: "https://images.unsplash.com/photo-1589367920969-ab8e050bbb04?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },

    // 3. Beverages
    { id: "PRD-011", name: "Nescafe Classic Coffee", code: "PRD-011", category: "Beverages", unit: "Unit", purchasePrice: 150, sellingPrice: 165, desc: "Instant coffee 50g jar.", imgUrl: "assets/images/products/gen_coffee.png", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-012", name: "Taj Mahal Tea", code: "PRD-012", category: "Beverages", unit: "Unit", purchasePrice: 130, sellingPrice: 145, desc: "Premium black tea 250g.", imgUrl: "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-013", name: "Red Label Tea", code: "PRD-013", category: "Beverages", unit: "Unit", purchasePrice: 240, sellingPrice: 260, desc: "Brooke Bond tea 500g.", imgUrl: "https://images.unsplash.com/photo-1597481499750-3e6b22637e12?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-014", name: "Coca-Cola", code: "PRD-014", category: "Beverages", unit: "Litre", purchasePrice: 40, sellingPrice: 45, desc: "Soft drink 1L bottle.", imgUrl: "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-015", name: "Frooti Mango Drink", code: "PRD-015", category: "Beverages", unit: "Litre", purchasePrice: 50, sellingPrice: 60, desc: "Mango juice 1L bottle.", imgUrl: "https://images.unsplash.com/photo-1546173159-315724a31696?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },

    // 4. Biscuits
    { id: "PRD-016", name: "Parle-G", code: "PRD-016", category: "Biscuits", unit: "Packet", purchasePrice: 70, sellingPrice: 80, desc: "Original glucose biscuits 800g.", imgUrl: "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-017", name: "Britannia Good Day", code: "PRD-017", category: "Biscuits", unit: "Packet", purchasePrice: 30, sellingPrice: 35, desc: "Cashew cookies 250g.", imgUrl: "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-018", name: "Sunfeast Dark Fantasy", code: "PRD-018", category: "Biscuits", unit: "Packet", purchasePrice: 90, sellingPrice: 110, desc: "Choco fill cookies 300g.", imgUrl: "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-019", name: "Oreo Chocolate", code: "PRD-019", category: "Biscuits", unit: "Packet", purchasePrice: 25, sellingPrice: 30, desc: "Chocolate sandwich cookies 120g.", imgUrl: "https://images.unsplash.com/photo-1569864358642-9d1684040f43?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-020", name: "ITC Marie Light", code: "PRD-020", category: "Biscuits", unit: "Packet", purchasePrice: 20, sellingPrice: 25, desc: "Light tea biscuits 200g.", imgUrl: "https://images.unsplash.com/photo-1590080875515-8a3a8dc5735e?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },

    // 5. Dairy
    { id: "PRD-021", name: "Amul Taaza Milk", code: "PRD-021", category: "Dairy", unit: "Litre", purchasePrice: 60, sellingPrice: 66, desc: "Toned milk 1L carton.", imgUrl: "assets/images/products/gen_milk.png", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-022", name: "Mother Dairy Paneer", code: "PRD-022", category: "Dairy", unit: "Unit", purchasePrice: 75, sellingPrice: 85, desc: "Fresh cottage cheese 200g.", imgUrl: "https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-023", name: "Gowardhan Ghee", code: "PRD-023", category: "Dairy", unit: "Litre", purchasePrice: 550, sellingPrice: 600, desc: "Pure cow ghee 1L.", imgUrl: "https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-024", name: "Nandini Butter", code: "PRD-024", category: "Dairy", unit: "Unit", purchasePrice: 240, sellingPrice: 265, desc: "Salted butter 500g.", imgUrl: "https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-025", name: "Epigamia Greek Yogurt", code: "PRD-025", category: "Dairy", unit: "Unit", purchasePrice: 35, sellingPrice: 45, desc: "Blueberry yogurt 120g.", imgUrl: "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },

    // 6. Grocery Essentials
    { id: "PRD-026", name: "Tata Salt", code: "PRD-026", category: "Grocery Essentials", unit: "Kg", purchasePrice: 20, sellingPrice: 25, desc: "Vacuum evaporated iodized salt.", imgUrl: "https://images.unsplash.com/photo-1518110168401-f28435863675?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-027", name: "Fortune Sunflower Oil", code: "PRD-027", category: "Grocery Essentials", unit: "Litre", purchasePrice: 120, sellingPrice: 140, desc: "Refined sunflower oil 1L.", imgUrl: "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-028", name: "India Gate Basmati Rice", code: "PRD-028", category: "Grocery Essentials", unit: "Kg", purchasePrice: 450, sellingPrice: 520, desc: "Classic basmati rice 5Kg.", imgUrl: "https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-029", name: "MDH Garam Masala", code: "PRD-029", category: "Grocery Essentials", unit: "Unit", purchasePrice: 70, sellingPrice: 82, desc: "Mixed spice powder 100g.", imgUrl: "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-030", name: "Everest Turmeric Powder", code: "PRD-030", category: "Grocery Essentials", unit: "Unit", purchasePrice: 45, sellingPrice: 55, desc: "Pure Haldi powder 200g.", imgUrl: "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },

    // 7. Snacks
    { id: "PRD-031", name: "Lays Classic Salted", code: "PRD-031", category: "Snacks", unit: "Packet", purchasePrice: 15, sellingPrice: 20, desc: "Potato chips 50g.", imgUrl: "https://images.unsplash.com/photo-1566478989037-eec170784d0b?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-032", name: "Haldiram Bhujia Sev", code: "PRD-032", category: "Snacks", unit: "Packet", purchasePrice: 45, sellingPrice: 55, desc: "Spicy Indian snack 200g.", imgUrl: "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-033", name: "Kurkure Masala Munch", code: "PRD-033", category: "Snacks", unit: "Packet", purchasePrice: 15, sellingPrice: 20, desc: "Crispy snack 90g.", imgUrl: "https://images.unsplash.com/photo-1599490659213-e2b9527bd087?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-034", name: "Bingo Mad Angles", code: "PRD-034", category: "Snacks", unit: "Packet", purchasePrice: 15, sellingPrice: 20, desc: "Achaari Masti 80g.", imgUrl: "https://images.unsplash.com/photo-1613919113640-25732ec5e61f?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-035", name: "Balaji Wafers", code: "PRD-035", category: "Snacks", unit: "Packet", purchasePrice: 15, sellingPrice: 20, desc: "Cream & Onion chips 65g.", imgUrl: "https://images.unsplash.com/photo-1528751014936-863e6e7a319c?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },

    // 8. Personal Care
    { id: "PRD-036", name: "Colgate MaxFresh", code: "PRD-036", category: "Personal Care", unit: "Unit", purchasePrice: 85, sellingPrice: 95, desc: "Cool Mint toothpaste 150g.", imgUrl: "https://images.unsplash.com/photo-1559598467-f8b76c8155d0?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-037", name: "Dove Soap", code: "PRD-037", category: "Personal Care", unit: "Unit", purchasePrice: 40, sellingPrice: 48, desc: "Cream beauty bathing bar 100g.", imgUrl: "https://images.unsplash.com/photo-1607006482172-3d5f3089d5f0?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-038", name: "Head & Shoulders", code: "PRD-038", category: "Personal Care", unit: "Unit", purchasePrice: 140, sellingPrice: 160, desc: "Anti-dandruff shampoo 180ml.", imgUrl: "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-039", name: "Gillette Mach 3", code: "PRD-039", category: "Personal Care", unit: "Unit", purchasePrice: 210, sellingPrice: 235, desc: "Shaving razor + 1 cartridge.", imgUrl: "https://images.unsplash.com/photo-1626285861696-9f0bf5a49c6d?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-040", name: "Nivea Body Lotion", code: "PRD-040", category: "Personal Care", unit: "Unit", purchasePrice: 195, sellingPrice: 220, desc: "Nourishing body lotion 200ml.", imgUrl: "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },

    // 9. Cleaning & Household
    { id: "PRD-041", name: "Surf Excel Matic", code: "PRD-041", category: "Cleaning", unit: "Kg", purchasePrice: 200, sellingPrice: 225, desc: "Top load detergent powder 1Kg.", imgUrl: "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-042", name: "Vim Dishwash Gel", code: "PRD-042", category: "Cleaning", unit: "Litre", purchasePrice: 130, sellingPrice: 145, desc: "Lemon dishwash gel 750ml.", imgUrl: "https://images.unsplash.com/photo-1585830810419-7ac6e4f8442b?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-043", name: "Lizol Floor Cleaner", code: "PRD-043", category: "Cleaning", unit: "Litre", purchasePrice: 155, sellingPrice: 175, desc: "Citrus floor cleaner 1L.", imgUrl: "https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-044", name: "Harpic Toilet Cleaner", code: "PRD-044", category: "Cleaning", unit: "Litre", purchasePrice: 135, sellingPrice: 150, desc: "Original power plus 1L.", imgUrl: "https://images.unsplash.com/photo-1563453392212-326f5e854473?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-045", name: "Colin Glass Cleaner", code: "PRD-045", category: "Cleaning", unit: "Unit", purchasePrice: 85, sellingPrice: 95, desc: "Glass and surface cleaner 500ml.", imgUrl: "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },

    // 10. Fresh Produce (Sample)
    { id: "PRD-046", name: "Farm Fresh Apples", code: "PRD-046", category: "Produce", unit: "Kg", purchasePrice: 120, sellingPrice: 140, desc: "Fresh Washington apples.", imgUrl: "assets/images/products/gen_apples.png", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-047", name: "Organic Bananas", code: "PRD-047", category: "Produce", unit: "Kg", purchasePrice: 40, sellingPrice: 55, desc: "Robusta bananas 1Kg.", imgUrl: "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-048", name: "Red Onions", code: "PRD-048", category: "Produce", unit: "Kg", purchasePrice: 25, sellingPrice: 35, desc: "Fresh red onions.", imgUrl: "https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-049", name: "Russet Potatoes", code: "PRD-049", category: "Produce", unit: "Kg", purchasePrice: 20, sellingPrice: 28, desc: "Premium quality potatoes.", imgUrl: "https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-050", name: "Fresh Tomatoes", code: "PRD-050", category: "Produce", unit: "Kg", purchasePrice: 30, sellingPrice: 45, desc: "Farm fresh tomatoes.", imgUrl: "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },

    // 11. Newly Added Products
    { id: "PRD-051", name: "Harpic Toilet Cleaner", code: "PRD-051", category: "Cleaning", unit: "Bottle", purchasePrice: 145, sellingPrice: 170, currentQuantity: 42, desc: "Harpic Toilet Cleaner", imgUrl: "https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-052", name: "Lizol Floor Cleaner", code: "PRD-052", category: "Cleaning", unit: "Bottle", purchasePrice: 165, sellingPrice: 195, currentQuantity: 38, desc: "Lizol Floor Cleaner", imgUrl: "https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-053", name: "Surf Excel Easy Wash", code: "PRD-053", category: "Household Essentials", unit: "Pack", purchasePrice: 185, sellingPrice: 220, currentQuantity: 47, desc: "Surf Excel Easy Wash", imgUrl: "https://images.unsplash.com/photo-1582735689369-4fe89db7114c?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-054", name: "Vim Dishwash Liquid", code: "PRD-054", category: "Household Essentials", unit: "Bottle", purchasePrice: 95, sellingPrice: 120, currentQuantity: 56, desc: "Vim Dishwash Liquid", imgUrl: "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-055", name: "Colgate Strong Teeth Toothpaste", code: "PRD-055", category: "Personal Care", unit: "Tube", purchasePrice: 82, sellingPrice: 99, currentQuantity: 64, desc: "Colgate Strong Teeth Toothpaste", imgUrl: "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() },
    { id: "PRD-056", name: "Dove Beauty Soap (Pack of 4)", code: "PRD-056", category: "Personal Care", unit: "Pack", purchasePrice: 165, sellingPrice: 195, currentQuantity: 35, desc: "Dove Beauty Soap (Pack of 4)", imgUrl: "https://images.unsplash.com/photo-1600857544200-b2f666a9a2ec?auto=format&fit=crop&w=400&q=80", status: "Available", createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() }
];

// 
// Initialize mock quantities
products.forEach(p => {
    if (p.currentQuantity === undefined) {
        p.currentQuantity = Math.floor(Math.random() * 100) + 10;
    }
});

let categories = [];

// Pagination State
let currentPage = 1;
const itemsPerPage = 10;
let currentViewMode = 'list';
const PIXABAY_API_KEY = 'YOUR_API_KEY';
const pixabayCache = {};

// DOM Elements
const tbody = document.getElementById('productTableBody');
const searchInput = document.getElementById('searchInput');
const categoryFilter = document.getElementById('categoryFilter');
const sortFilter = document.getElementById('sortFilter');
const refreshBtn = document.getElementById('refreshBtn');

const prevPageBtn = document.getElementById('prevPageBtn');
const nextPageBtn = document.getElementById('nextPageBtn');
const pageNumbers = document.getElementById('pageNumbers');
const paginationInfo = document.getElementById('paginationInfo');
const toastContainer = document.getElementById('toastContainer');

// Modals
const addProductModal = document.getElementById('addProductModal');
const editProductModal = document.getElementById('editProductModal');
const viewProductModal = document.getElementById('viewProductModal');
const deleteConfirmModal = document.getElementById('deleteConfirmModal');
const addCategoryModal = document.getElementById('addCategoryModal');

function populateCategoryDropdowns() {
    const extracted = products.map(p => p.category);
    categories = [...new Set(extracted)].filter(Boolean).sort();
    
    const addCat = document.getElementById('addCategory');
    const editCat = document.getElementById('editCategory');
    
    const currentAddVal = addCat.value;
    const currentEditVal = editCat.value;
    
    if (addCat) addCat.innerHTML = '<option value="">Select Category</option>';
    if (editCat) editCat.innerHTML = '<option value="">Select Category</option>';
    
    categories.forEach(cat => {
        if (addCat) addCat.add(new Option(cat, cat));
        if (editCat) editCat.add(new Option(cat, cat));
    });
    
    if (addCat) addCat.value = currentAddVal;
    if (editCat) editCat.value = currentEditVal;

    const filterInput = document.getElementById('categoryFilter');
    const categoryOptions = document.getElementById('categoryOptions');
    if(categoryOptions && filterInput) {
        const currentFilterVal = filterInput.value;
        let html = `<div class="dropdown-option ${currentFilterVal === '' ? 'selected' : ''}" data-value="">
                        <span>All Categories</span>
                        <i class="fa-solid fa-check check-icon"></i>
                    </div>`;
        categories.forEach(cat => {
            html += `<div class="dropdown-option ${currentFilterVal === cat ? 'selected' : ''}" data-value="${cat}">
                        <span>${cat}</span>
                        <i class="fa-solid fa-check check-icon"></i>
                    </div>`;
        });
        categoryOptions.innerHTML = html;
        
        const options = categoryOptions.querySelectorAll('.dropdown-option');
        options.forEach(opt => {
            opt.addEventListener('click', (e) => {
                e.stopPropagation();
                options.forEach(o => o.classList.remove('selected'));
                opt.classList.add('selected');
                
                filterInput.value = opt.getAttribute('data-value');
                document.querySelector('#categorySelected span').textContent = opt.querySelector('span').textContent;
                
                document.getElementById('categoryDropdown').classList.remove('open');
                currentPage = 1;
                renderTable();
            });
        });
    }
}

// Product-Accurate Image Dictionary Map
const PRODUCT_IMAGE_MAP = {
    'atta': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=400&q=80',
    'besan': 'https://images.unsplash.com/photo-1627485937980-221c88ab04f9?auto=format&fit=crop&w=400&q=80',
    'maida': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&q=80',
    'bread': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=400&q=80',
    'buns': 'https://images.unsplash.com/photo-1586190848861-99aa4a171e90?auto=format&fit=crop&w=400&q=80',
    'garlic bread': 'https://images.unsplash.com/photo-1619535860434-ba1d8fa12536?auto=format&fit=crop&w=400&q=80',
    'coffee': 'https://images.unsplash.com/photo-1559056199-641a0ac8b55e?auto=format&fit=crop&w=400&q=80',
    'tea': 'https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=400&q=80',
    'coca-cola': 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=400&q=80',
    'cola': 'https://images.unsplash.com/photo-1622483767028-3f66f32aef97?auto=format&fit=crop&w=400&q=80',
    'mango': 'https://images.unsplash.com/photo-1546173159-315724a31696?auto=format&fit=crop&w=400&q=80',
    'frooti': 'https://images.unsplash.com/photo-1546173159-315724a31696?auto=format&fit=crop&w=400&q=80',
    'parle': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?auto=format&fit=crop&w=400&q=80',
    'biscuit': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?auto=format&fit=crop&w=400&q=80',
    'good day': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=400&q=80',
    'cookies': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=400&q=80',
    'oreo': 'https://images.unsplash.com/photo-1569864358642-9d1684040f43?auto=format&fit=crop&w=400&q=80',
    'milk': 'https://images.unsplash.com/photo-1563636619-e9143da7973b?auto=format&fit=crop&w=400&q=80',
    'paneer': 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?auto=format&fit=crop&w=400&q=80',
    'ghee': 'https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?auto=format&fit=crop&w=400&q=80',
    'butter': 'https://images.unsplash.com/photo-1589985270826-4b7bb135bc9d?auto=format&fit=crop&w=400&q=80',
    'yogurt': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=400&q=80',
    'salt': 'https://images.unsplash.com/photo-1518110168401-f28435863675?auto=format&fit=crop&w=400&q=80',
    'oil': 'https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?auto=format&fit=crop&w=400&q=80',
    'rice': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=400&q=80',
    'masala': 'https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=400&q=80',
    'turmeric': 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=400&q=80',
    'chips': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?auto=format&fit=crop&w=400&q=80',
    'lays': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?auto=format&fit=crop&w=400&q=80',
    'bhujia': 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?auto=format&fit=crop&w=400&q=80',
    'kurkure': 'https://images.unsplash.com/photo-1621939514649-280e2ee25f60?auto=format&fit=crop&w=400&q=80',
    'bingo': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?auto=format&fit=crop&w=400&q=80',
    'wafers': 'https://images.unsplash.com/photo-1566478989037-eec170784d0b?auto=format&fit=crop&w=400&q=80',
    'colgate': 'https://images.unsplash.com/photo-1559598467-f8b76c8155d0?auto=format&fit=crop&w=400&q=80',
    'toothpaste': 'https://images.unsplash.com/photo-1559598467-f8b76c8155d0?auto=format&fit=crop&w=400&q=80',
    'soap': 'https://images.unsplash.com/photo-1607006482172-3d5f3089d5f0?auto=format&fit=crop&w=400&q=80',
    'dove': 'https://images.unsplash.com/photo-1607006482172-3d5f3089d5f0?auto=format&fit=crop&w=400&q=80',
    'shampoo': 'https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?auto=format&fit=crop&w=400&q=80',
    'razor': 'https://images.unsplash.com/photo-1626285861696-9f0bf5a49c6d?auto=format&fit=crop&w=400&q=80',
    'gillette': 'https://images.unsplash.com/photo-1626285861696-9f0bf5a49c6d?auto=format&fit=crop&w=400&q=80',
    'lotion': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=400&q=80',
    'nivea': 'https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?auto=format&fit=crop&w=400&q=80',
    'surf': 'https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?auto=format&fit=crop&w=400&q=80',
    'detergent': 'https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?auto=format&fit=crop&w=400&q=80',
    'vim': 'https://images.unsplash.com/photo-1585830810419-7ac6e4f8442b?auto=format&fit=crop&w=400&q=80',
    'dishwash': 'https://images.unsplash.com/photo-1585830810419-7ac6e4f8442b?auto=format&fit=crop&w=400&q=80',
    'lizol': 'https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?auto=format&fit=crop&w=400&q=80',
    'floor cleaner': 'https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?auto=format&fit=crop&w=400&q=80',
    'harpic': 'https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?auto=format&fit=crop&w=400&q=80',
    'toilet cleaner': 'https://images.unsplash.com/photo-1584820927498-cfe5211fd8bf?auto=format&fit=crop&w=400&q=80',
    'colin': 'https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?auto=format&fit=crop&w=400&q=80',
    'glass cleaner': 'https://images.unsplash.com/photo-1585421514284-efb74c2b69ba?auto=format&fit=crop&w=400&q=80',
    'apples': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=400&q=80',
    'bananas': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=400&q=80',
    'onions': 'https://images.unsplash.com/photo-1618512496248-a07fe83aa8cb?auto=format&fit=crop&w=400&q=80',
    'potatoes': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=400&q=80',
    'tomatoes': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=400&q=80'
};

// Pixabay API & Automated Image Resolver
async function resolveImage(productName, imgElement) {
    if (!productName || !imgElement) return;
    const cleanName = productName.replace(/\(.*?\)/g, '').trim().toLowerCase();

    if (pixabayCache[cleanName]) {
        imgElement.src = pixabayCache[cleanName];
        return;
    }

    if (PIXABAY_API_KEY && PIXABAY_API_KEY !== 'YOUR_API_KEY') {
        try {
            const res = await fetch(`https://pixabay.com/api/?key=${PIXABAY_API_KEY}&q=${encodeURIComponent(cleanName)}&image_type=photo&per_page=3`);
            const data = await res.json();
            if (data && data.hits && data.hits.length > 0) {
                const url = data.hits[0].webformatURL || data.hits[0].previewURL;
                pixabayCache[cleanName] = url;
                imgElement.src = url;
                return;
            }
        } catch(e) {
            console.error("Pixabay fetch failed", e);
        }
    }

    // Match related high-resolution product image from PRODUCT_IMAGE_MAP
    for (const [key, mapUrl] of Object.entries(PRODUCT_IMAGE_MAP)) {
        if (cleanName.includes(key)) {
            pixabayCache[cleanName] = mapUrl;
            imgElement.src = mapUrl;
            return;
        }
    }

    // Default grocery item photo if no specific keyword matched
    const defaultGroceryUrl = 'https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=400&q=80';
    pixabayCache[cleanName] = defaultGroceryUrl;
    imgElement.src = defaultGroceryUrl;
}

function handleImgError(imgEl, productName) {
    if (imgEl.dataset.fallbackTried) return;
    imgEl.dataset.fallbackTried = 'true';
    resolveImage(productName, imgEl);
}

// Render Engine
function renderTable() {
    // Clean up any detached menus in body to prevent leaks
    document.querySelectorAll('body > .action-menu-dropdown').forEach(m => m.remove());

    let filtered = products;

    // Search filter
    const term = searchInput.value.toLowerCase();
    if (term) {
        filtered = filtered.filter(p => 
            p.name.toLowerCase().includes(term) || 
            p.code.toLowerCase().includes(term)
        );
    }

    // Category filter
    const cat = categoryFilter.value;
    if (cat) {
        filtered = filtered.filter(p => p.category === cat);
    }

    // Sorting
    const sort = sortFilter.value;
    if (sort === 'name-asc') {
        filtered.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sort === 'name-desc') {
        filtered.sort((a, b) => b.name.localeCompare(a.name));
    } else if (sort === 'price-asc') {
        filtered.sort((a, b) => a.sellingPrice - b.sellingPrice);
    } else if (sort === 'price-desc') {
        filtered.sort((a, b) => b.sellingPrice - a.sellingPrice);
    } else if (sort === 'recently-added') {
        filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    }

    // Pagination
    const totalItems = filtered.length;
    const totalPages = Math.ceil(totalItems / itemsPerPage) || 1;
    
    if (currentPage > totalPages) currentPage = totalPages;
    if (currentPage < 1) currentPage = 1;
    
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, totalItems);
    
    const paginatedItems = filtered.slice(startIndex, endIndex);

    // Update Pagination UI
    paginationInfo.textContent = `Showing ${totalItems === 0 ? 0 : startIndex + 1}–${endIndex} of ${totalItems} Products`;
    prevPageBtn.disabled = currentPage === 1;
    nextPageBtn.disabled = currentPage === totalPages;
    
    pageNumbers.innerHTML = '';
    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.className = `page-btn ${i === currentPage ? 'active' : ''}`;
        btn.textContent = i;
        btn.onclick = () => { currentPage = i; renderTable(); };
        pageNumbers.appendChild(btn);
    }

    tbody.innerHTML = '';
    const gridBody = document.getElementById('productGridBody');
    if (gridBody) gridBody.innerHTML = '';

    const tableContainer = document.querySelector('.table-container');
    const gridContainer = document.getElementById('productGridContainer');

    if (currentViewMode === 'grid') {
        if (tableContainer) tableContainer.style.display = 'none';
        if (gridContainer) gridContainer.style.display = 'block';
    } else {
        if (tableContainer) tableContainer.style.display = 'block';
        if (gridContainer) gridContainer.style.display = 'none';
    }

    if (paginatedItems.length === 0) {
        if (currentViewMode === 'list') {
            tbody.innerHTML = `<tr><td colspan="9" style="text-align:center; padding: 24px; color: #64748b;">
                <div style="font-weight: 600; font-size: 15px; color: #334155;">No products found.</div>
                <div style="font-size: 13px; margin-top: 4px;">Try another search or reset filters.</div>
            </td></tr>`;
        } else if (gridBody) {
            gridBody.innerHTML = `<div style="grid-column: 1 / -1; text-align:center; padding: 40px; color: #64748b;">
                <div style="font-weight: 600; font-size: 15px; color: #334155;">No products found.</div>
                <div style="font-size: 13px; margin-top: 4px;">Try another search or reset filters.</div>
            </div>`;
        }
        return;
    }

    paginatedItems.forEach((p, index) => {
        const fallbackSrc = 'assets/images/products/fallback.png';
        const imgSrc = p.imgUrl || fallbackSrc;
        const needsPixabay = imgSrc.includes(fallbackSrc) || imgSrc.includes('PRD-');

        if (currentViewMode === 'list') {
            const tr = document.createElement('tr');
            tr.style.animationDelay = `${index * 50}ms`;
            tr.innerHTML = `
                <td><img src="${imgSrc}" alt="${p.name}" class="product-thumb" onerror="handleImgError(this, '${p.name.replace(/'/g, "\\'")}')"></td>
                <td title="${p.name}"><span class="product-name-trunc">${p.name}</span></td>
                <td>${p.code}</td>
                <td>${p.category}</td>
                <td><span style="font-weight:600; color:var(--color-primary);">${p.currentQuantity}</span> ${p.unit}</td>
                <td style="text-align: right;">₹${p.purchasePrice.toFixed(2)}</td>
                <td style="text-align: right;">₹${p.sellingPrice.toFixed(2)}</td>
                <td style="text-align: center;"><span style="padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; background-color: ${p.status === 'Available' ? '#dcfce7' : '#fee2e2'}; color: ${p.status === 'Available' ? '#166534' : '#991b1b'};">${p.status}</span></td>
                <td style="text-align: center;">
                    <div class="action-menu-container">
                        <button class="action-menu-btn" onclick="toggleActionMenu('${p.id}', event)">
                            <i class="fa-solid fa-ellipsis-vertical"></i>
                        </button>
                        <div class="action-menu-dropdown" id="action-menu-${p.id}">
                            <a href="javascript:void(0)" onclick="openViewModal('${p.id}')"><i class="fa-solid fa-eye"></i> View</a>
                            <a href="javascript:void(0)" onclick="openEditModal('${p.id}')"><i class="fa-solid fa-pen"></i> Edit</a>
                            <a href="javascript:void(0)" class="delete-action" onclick="openDeleteModal('${p.id}')"><i class="fa-solid fa-trash"></i> Delete</a>
                        </div>
                    </div>
                </td>
            `;
            tbody.appendChild(tr);
            if (needsPixabay) {
                const imgEl = tr.querySelector('img');
                resolveImage(p.name, imgEl);
            }
        } else if (gridBody) {
            const card = document.createElement('div');
            card.className = 'grid-card';
            card.style.animation = `fadeSlideUp 0.3s ease forwards ${index * 50}ms`;
            card.innerHTML = `
                <div class="grid-card-img">
                    <img src="${imgSrc}" alt="${p.name}" onerror="handleImgError(this, '${p.name.replace(/'/g, "\\'")}')">
                    <div class="grid-card-menu" onclick="toggleActionMenu('${p.id}', event)">
                        <i class="fa-solid fa-ellipsis-vertical" style="color: #64748b;"></i>
                    </div>
                </div>
                <div class="grid-card-body">
                    <div class="grid-card-title" title="${p.name}">${p.name}</div>
                    <div class="grid-card-subtitle" style="margin-bottom: 4px;"><strong>SKU:</strong> ${p.code}</div>
                    <div class="grid-card-subtitle" style="margin-bottom: 4px;"><strong>Category:</strong> ${p.category}</div>
                    <div class="grid-card-subtitle" style="margin-bottom: 8px;"><strong>Status:</strong> <span style="color: ${p.status === 'Available' ? '#166534' : '#991b1b'}; font-weight: 500;">${p.status}</span></div>
                    <div class="grid-card-stats">
                        <div class="grid-card-stat">
                            <span class="grid-card-stat-label">Qty</span>
                            <span class="grid-card-stat-val" style="color: var(--color-primary);">${p.currentQuantity} ${p.unit}</span>
                        </div>
                        <div class="grid-card-stat" style="align-items: flex-end;">
                            <span class="grid-card-stat-label">Buy Price</span>
                            <span class="grid-card-stat-val">₹${p.purchasePrice.toFixed(2)}</span>
                        </div>
                    </div>
                    <div class="grid-card-price">
                        <small>Sell Price</small>
                        <span>₹${p.sellingPrice.toFixed(2)}</span>
                    </div>
                </div>
                <div class="action-menu-dropdown" id="action-menu-${p.id}" style="display: none; position: absolute; top: 40px; right: 8px;">
                    <a href="javascript:void(0)" onclick="openViewModal('${p.id}')"><i class="fa-solid fa-eye"></i> View</a>
                    <a href="javascript:void(0)" onclick="openEditModal('${p.id}')"><i class="fa-solid fa-pen"></i> Edit</a>
                    <a href="javascript:void(0)" class="delete-action" onclick="openDeleteModal('${p.id}')"><i class="fa-solid fa-trash"></i> Delete</a>
                </div>
            `;
            gridBody.appendChild(card);
            if (needsPixabay) {
                const imgEl = card.querySelector('img');
                resolveImage(p.name, imgEl);
            }
        }
    });
}

// Toast System
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const icon = type === 'success' ? '<i class="fa-solid fa-circle-check toast-icon"></i>' : '<i class="fa-solid fa-circle-xmark toast-icon"></i>';
    
    toast.innerHTML = `
        ${icon}
        <span class="toast-msg">${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // Animate in
    setTimeout(() => { toast.classList.add('show'); }, 10);
    
    // Auto remove
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);

    // Add to Notification Dropdown
    if (type === 'success' || type === 'undo') {
        addNotificationToDropdown(message);
    }
}

function addNotificationToDropdown(message) {
    const notifList = document.getElementById('notificationList');
    const notifBadge = document.getElementById('notificationBadge');
    if (notifList && notifBadge) {
        const emptyState = notifList.querySelector('.empty-state');
        if (emptyState) emptyState.remove();

        const item = document.createElement('div');
        item.className = 'notification-item';
        
        const timeString = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute:'2-digit' });
        
        item.innerHTML = `
            <div class="unread-dot"></div>
            <div class="notification-icon">
                <i class="fa-solid fa-bell"></i>
            </div>
            <div class="notification-text" style="flex:1;">
                <p>${message}</p>
                <small>${timeString}</small>
            </div>
            <i class="fa-solid fa-xmark dismiss-notif" title="Dismiss"></i>
        `;
        
        item.querySelector('.dismiss-notif').addEventListener('click', (e) => {
            e.stopPropagation();
            item.classList.add('notif-dismissing');
            setTimeout(() => {
                item.remove();
                checkEmptyNotifications();
            }, 300);
        });
        
        notifList.prepend(item);
        
        const count = parseInt(notifBadge.textContent) || 0;
        notifBadge.textContent = count + 1;
        notifBadge.style.display = 'flex';
    }
}

function checkEmptyNotifications() {
    const notifList = document.getElementById('notificationList');
    if (notifList && !notifList.querySelector('.notification-item')) {
        notifList.innerHTML = `
            <div class="empty-state" style="padding:48px 24px; text-align:center; color:#94a3b8;">
                <i class="fa-regular fa-bell-slash" style="font-size:32px; margin-bottom:12px; color:#cbd5e1;"></i>
                <div style="font-size:15px; font-weight:500; color:#475569;">No notifications available.</div>
                <div style="font-size:13px; margin-top:4px;">You're all caught up!</div>
            </div>
        `;
    }
}

// Undo Variables
let deletedProductData = null;
let deletedProductIndex = -1;

function showUndoToast(message) {
    const toast = document.createElement('div');
    toast.className = `toast toast-success`;
    
    toast.innerHTML = `
        <i class="fa-solid fa-circle-check toast-icon"></i>
        <span class="toast-msg" style="flex:1;">${message}</span>
        <button id="undoDeleteBtn" style="background:none; border:none; color:var(--color-primary); font-weight:600; cursor:pointer;">UNDO</button>
    `;
    
    toastContainer.appendChild(toast);
    setTimeout(() => { toast.classList.add('show'); }, 10);
    
    let hideTimeout = setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
        deletedProductData = null;
    }, 5000);

    const undoBtn = toast.querySelector('#undoDeleteBtn');
    undoBtn.addEventListener('click', () => {
        clearTimeout(hideTimeout);
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
        
        if (deletedProductData) {
            products.splice(deletedProductIndex, 0, deletedProductData);
            deletedProductData = null;
            populateCategoryDropdowns();
            renderTable();
            showToast('Product Restored', 'undo');
        }
    });
    
    addNotificationToDropdown(message);
}

// Initial Render
document.addEventListener('DOMContentLoaded', () => {
    populateCategoryDropdowns();
    // Custom Dropdown UI interactions
    const categoryDropdown = document.getElementById('categoryDropdown');
    const sortDropdown = document.getElementById('sortDropdown');

    if (categoryDropdown) {
        categoryDropdown.addEventListener('click', (e) => {
            e.stopPropagation();
            if (sortDropdown) sortDropdown.classList.remove('open');
            categoryDropdown.classList.toggle('open');
        });
    }
    
    if (sortDropdown) {
        sortDropdown.addEventListener('click', (e) => {
            e.stopPropagation();
            if (categoryDropdown) categoryDropdown.classList.remove('open');
            sortDropdown.classList.toggle('open');
        });
        
        const sortOptions = sortDropdown.querySelectorAll('.dropdown-option');
        const sortFilterInput = document.getElementById('sortFilter');
        const sortSelectedText = document.querySelector('#sortSelected span');
        
        sortOptions.forEach(opt => {
            opt.addEventListener('click', (e) => {
                e.stopPropagation();
                sortOptions.forEach(o => o.classList.remove('selected'));
                opt.classList.add('selected');
                
                sortFilterInput.value = opt.getAttribute('data-value');
                sortSelectedText.textContent = opt.querySelector('span').textContent;
                
                sortDropdown.classList.remove('open');
                currentPage = 1;
                renderTable();
            });
        });
    }

    document.addEventListener('click', (e) => {
        if (categoryDropdown && !categoryDropdown.contains(e.target)) {
            categoryDropdown.classList.remove('open');
        }
        if (sortDropdown && !sortDropdown.contains(e.target)) {
            sortDropdown.classList.remove('open');
        }
    });
    
    renderTable();

    // Listeners for Action Bar
    const clearSearchBtn = document.getElementById('clearSearchBtn');
    const resetToPageOne = () => { 
        currentPage = 1; 
        if (searchInput.value.trim() !== '') {
            clearSearchBtn.style.display = 'block';
        } else {
            clearSearchBtn.style.display = 'none';
        }
        renderTable(); 
    };
    searchInput.addEventListener('input', resetToPageOne);
    clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        resetToPageOne();
    });
    // Note: custom categoryDropdown calls renderTable() directly on option click.
    // Note: custom sortDropdown calls renderTable() directly on option click.

    refreshBtn.addEventListener('click', () => {
        const icon = refreshBtn.querySelector('i');
        if (icon) {
            icon.classList.add('rotating');
            setTimeout(() => icon.classList.remove('rotating'), 500);
        }
        searchInput.value = '';
        if(clearSearchBtn) clearSearchBtn.style.display = 'none';
        if(categoryFilter) categoryFilter.value = '';
        const defaultCatOpt = document.querySelector('#categoryOptions .dropdown-option[data-value=""]');
        if(defaultCatOpt) {
            document.querySelectorAll('#categoryOptions .dropdown-option').forEach(o => o.classList.remove('selected'));
            defaultCatOpt.classList.add('selected');
            document.querySelector('#categorySelected span').textContent = 'All Categories';
        }
        if(sortFilter) sortFilter.value = '';
        const defaultSortOpt = document.querySelector('#sortOptions .dropdown-option[data-value=""]');
        if(defaultSortOpt) {
            document.querySelectorAll('#sortOptions .dropdown-option').forEach(o => o.classList.remove('selected'));
            defaultSortOpt.classList.add('selected');
            document.querySelector('#sortSelected span').textContent = 'Sort By';
        }
        currentPage = 1;
        renderTable();
        showToast('Products refreshed successfully.');
    });

    // View Toggle Listeners
    const listViewBtn = document.getElementById('listViewBtn');
    const gridViewBtn = document.getElementById('gridViewBtn');
    if (listViewBtn && gridViewBtn) {
        listViewBtn.addEventListener('click', () => {
            currentViewMode = 'list';
            listViewBtn.classList.add('active');
            gridViewBtn.classList.remove('active');
            renderTable();
        });
        gridViewBtn.addEventListener('click', () => {
            currentViewMode = 'grid';
            gridViewBtn.classList.add('active');
            listViewBtn.classList.remove('active');
            renderTable();
        });
    }

    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) { currentPage--; renderTable(); }
    });
    
    nextPageBtn.addEventListener('click', () => {
        currentPage++; renderTable();
    });

    // Add Product Modal Opens
    document.getElementById('openAddProductModal').addEventListener('click', () => {
        document.getElementById('addProductForm').reset();
        // Generate SKU
        let maxSku = 0;
        products.forEach(p => {
            const num = parseInt(p.code.replace('PRD-', ''), 10);
            if (!isNaN(num) && num > maxSku) maxSku = num;
        });
        const nextSku = `PRD-${String(maxSku + 1).padStart(3, '0')}`;
        document.getElementById('addCode').value = nextSku;
        openModal(addProductModal);
    });

    // Add Product Submit
    document.getElementById('addProductForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const code = document.getElementById('addCode').value.trim();
        const openingQuantity = parseInt(document.getElementById('addQuantity').value) || 0;
        const purchasePrice = parseFloat(document.getElementById('addPurchase').value);
        const sellingPrice = parseFloat(document.getElementById('addSelling').value);
        
        // Validation: Unique Code
        if (products.some(p => p.code.toLowerCase() === code.toLowerCase())) {
            showToast('Product Code already exists!', 'error');
            return;
        }
        
        // Validation: Price
        if (sellingPrice < purchasePrice) {
            showToast('Selling Price cannot be lower than Purchase Price!', 'error');
            return;
        }

        const newProduct = {
            id: code,
            name: document.getElementById('addName').value.trim(),
            code: code,
            category: document.getElementById('addCategory').value,
            unit: document.getElementById('addUnit').value,
            currentQuantity: openingQuantity,
            purchasePrice: purchasePrice,
            sellingPrice: sellingPrice,
            desc: document.getElementById('addDesc').value.trim(),
            imgUrl: document.getElementById('addImgUrl').value.trim() || 'assets/images/products/fallback.png',
            status: "Available",
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
        };
        products.push(newProduct);
        populateCategoryDropdowns();
        closeModal(addProductModal);
        showToast('Product Added Successfully');
        renderTable();
    });

    // Edit Product Submit
    document.getElementById('editProductForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const id = document.getElementById('editProductId').value;
        const index = products.findIndex(p => p.id === id);
        
        if (index > -1) {
            const code = document.getElementById('editCode').value.trim();
            const purchasePrice = parseFloat(document.getElementById('editPurchase').value);
            const sellingPrice = parseFloat(document.getElementById('editSelling').value);
            
            // Validation: Unique Code
            if (products.some(p => p.id !== id && p.code.toLowerCase() === code.toLowerCase())) {
                showToast('Product Code already exists!', 'error');
                return;
            }
            
            // Validation: Price
            if (sellingPrice < purchasePrice) {
                showToast('Selling Price cannot be lower than Purchase Price!', 'error');
                return;
            }

            products[index] = {
                ...products[index],
                name: document.getElementById('editName').value.trim(),
                code: code,
                category: document.getElementById('editCategory').value,
                unit: document.getElementById('editUnit').value,
                purchasePrice: purchasePrice,
                sellingPrice: sellingPrice,
                desc: document.getElementById('editDesc').value.trim(),
                imgUrl: document.getElementById('editImgUrl').value.trim() || products[index].imgUrl,
                updatedAt: new Date().toISOString()
            };
            populateCategoryDropdowns();
            closeModal(editProductModal);
            showToast('Product Updated Successfully');
            renderTable();
        }
    });

    // Delete Submit
    document.getElementById('confirmDeleteBtn').addEventListener('click', () => {
        const id = document.getElementById('deleteProductId').value;
        deletedProductIndex = products.findIndex(p => p.id === id);
        if (deletedProductIndex > -1) {
            deletedProductData = products[deletedProductIndex];
            products.splice(deletedProductIndex, 1);
            
            populateCategoryDropdowns();
            closeModal(deleteConfirmModal);
            
            // Adjust page if we deleted the last item on the current page
            const totalPages = Math.ceil(products.length / itemsPerPage) || 1;
            if (currentPage > totalPages) currentPage = totalPages;
            
            renderTable();
            showUndoToast('Product Deleted Successfully');
        }
    });

    // Notification Actions
    document.getElementById('markReadBtn')?.addEventListener('click', () => {
        const notifBadge = document.getElementById('notificationBadge');
        if (notifBadge) {
            notifBadge.textContent = '0';
            notifBadge.style.display = 'none';
        }
        document.querySelectorAll('.unread-dot').forEach(dot => {
            dot.style.opacity = '0';
            dot.style.transform = 'scale(0)';
            setTimeout(() => dot.remove(), 300);
        });
    });

    document.getElementById('clearNotifBtn')?.addEventListener('click', () => {
        const notifList = document.getElementById('notificationList');
        const notifBadge = document.getElementById('notificationBadge');
        
        if (notifBadge) {
            notifBadge.textContent = '0';
            notifBadge.style.display = 'none';
        }
        
        if (notifList) {
            const items = notifList.querySelectorAll('.notification-item');
            if (items.length > 0) {
                items.forEach((item, index) => {
                    setTimeout(() => {
                        item.classList.add('notif-dismissing');
                        setTimeout(() => item.remove(), 300);
                    }, index * 60);
                });
                setTimeout(() => checkEmptyNotifications(), (items.length * 60) + 300);
            } else {
                checkEmptyNotifications();
            }
        }
    });

    // Add Category Modal
    document.getElementById('addCategoryLink').addEventListener('click', (e) => {
        e.preventDefault();
        openModal(addCategoryModal);
    });

    document.getElementById('saveCategoryBtn').addEventListener('click', () => {
        const newCat = document.getElementById('newCategoryName').value.trim();
        if (newCat && !categories.includes(newCat)) {
            categories.push(newCat);
            populateCategoryDropdowns();
            document.getElementById('newCategoryName').value = '';
            showToast('Category Added Successfully');
        }
        closeModal(addCategoryModal);
    });

    // Modal Closing Logic
    document.querySelectorAll('.close-modal, .close-nested-modal').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const modal = e.target.closest('.modal-overlay');
            if(modal) closeModal(modal);
        });
    });

    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal-overlay')) {
            closeModal(e.target);
        }
    });

    // Close Modals on ESC key
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay.active').forEach(modal => {
                closeModal(modal);
            });
        }
    });
});

// Helper Functions
function openModal(modalEl) {
    if (modalEl) modalEl.classList.add('active');
}

function closeModal(modalEl) {
    if (modalEl) modalEl.classList.remove('active');
}

function formatDate(isoStr) {
    if (!isoStr) return 'N/A';
    const d = new Date(isoStr);
    return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) + ' ' + 
           d.toLocaleTimeString('en-US', { hour: '2-digit', minute:'2-digit' });
}

// Global functions for inline HTML event handlers
window.openViewModal = function(id) {
    const p = products.find(prod => prod.id === id);
    if (!p) return;
    document.getElementById('viewImg').src = p.imgUrl || '';
    document.getElementById('viewName').textContent = p.name;
    document.getElementById('viewCode').textContent = p.code;
    document.getElementById('viewCategory').textContent = p.category;
    document.getElementById('viewUnit').textContent = p.unit;
    document.getElementById('viewQuantity').textContent = `${p.currentQuantity || 0} ${p.unit}`;
    document.getElementById('viewPurchase').textContent = '₹' + p.purchasePrice.toFixed(2);
    document.getElementById('viewSelling').textContent = '₹' + p.sellingPrice.toFixed(2);
    document.getElementById('viewStatus').textContent = p.status || 'Available';
    document.getElementById('viewDesc').textContent = p.desc || 'N/A';
    
    document.getElementById('viewCreated').textContent = formatDate(p.createdAt);
    if (p.createdAt === p.updatedAt) {
        document.getElementById('viewUpdated').textContent = "Same as Created Date";
    } else {
        document.getElementById('viewUpdated').textContent = formatDate(p.updatedAt);
    }
    openModal(viewProductModal);
};

window.openEditModal = function(id) {
    const p = products.find(prod => prod.id === id);
    if (!p) return;
    document.getElementById('editProductId').value = p.id;
    document.getElementById('editImgUrl').value = p.imgUrl || '';
    document.getElementById('editName').value = p.name;
    document.getElementById('editCode').value = p.code;
    document.getElementById('editCategory').value = p.category;
    document.getElementById('editUnit').value = p.unit;
    document.getElementById('editQuantity').value = `${p.currentQuantity || 0} ${p.unit}`;
    document.getElementById('editPurchase').value = p.purchasePrice;
    document.getElementById('editSelling').value = p.sellingPrice;
    document.getElementById('editDesc').value = p.desc || '';
    openModal(editProductModal);
};

window.openDeleteModal = function(id) {
    document.getElementById('deleteProductId').value = id;
    openModal(deleteConfirmModal);
};

window.toggleActionMenu = function(id, event) {
    event.stopPropagation();
    
    // Reset all row z-indexes
    document.querySelectorAll('.data-table tbody tr').forEach(tr => {
        tr.style.zIndex = '';
    });

    const allMenus = document.querySelectorAll('.action-menu-dropdown');
    allMenus.forEach(menu => {
        if (menu.id !== `action-menu-${id}`) {
            menu.classList.remove('show');
            menu.style.display = '';
        }
    });
    
    const menu = document.getElementById(`action-menu-${id}`);
    if (menu) {
        menu.classList.toggle('show');
        if (menu.classList.contains('show')) {
            // Move menu to the body to escape all overflow and backdrop-filter clipping containers
            if (menu.parentElement !== document.body) {
                document.body.appendChild(menu);
            }

            const btn = event.currentTarget;
            const btnRect = btn.getBoundingClientRect();
            
            menu.style.display = 'flex'; // Make visible to measure height
            const menuRect = menu.getBoundingClientRect();
            
            // Default downwards
            let topPos = btnRect.bottom;
            
            // If it goes off the bottom of the screen, flip upwards
            if (topPos + menuRect.height > window.innerHeight) {
                topPos = btnRect.top - menuRect.height;
            }
            
            menu.style.top = `${topPos}px`;
            // Align right edge of menu to right edge of button
            menu.style.left = `${btnRect.right - menuRect.width}px`;
            
            // Elevate row visually just in case
            const tr = document.querySelector(`.action-menu-dropdown[id="action-menu-${id}"]`)?.closest('tr');
            if (tr) tr.style.zIndex = '999';
        } else {
            menu.style.display = '';
        }
    }
};

document.addEventListener('click', function(event) {
    if (!event.target.closest('.action-menu-container')) {
        const allMenus = document.querySelectorAll('.action-menu-dropdown');
        allMenus.forEach(menu => {
            menu.classList.remove('show');
            menu.style.display = '';
        });
        // Reset all row z-indexes
        document.querySelectorAll('.data-table tbody tr').forEach(tr => {
            tr.style.zIndex = '';
        });
    }
});
