import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc

import dash
from dash import html, dcc
import dash_mantine_components as dmc

dash.register_page(__name__, path="/projects/order-book", name="Order Book")

layout = dmc.Container(
    children=[
        dmc.Title("Order Book Construction", order=1),
        dmc.Space(h=30),
        dmc.Stack(
            [
                dmc.Group(
                    [
                        dmc.Badge("C++", size="lg", variant="dot"),
                        dmc.Badge("Order Book Arquitecture", size="lg", variant="dot"),
                        dmc.Badge("Cache Locality", size="lg", variant="dot"),
                        dmc.Badge("Memory bookeeping", size="lg", variant="dot"),
                    ]
                ),
                dmc.Text("Published: Mar 6, 2026", style={"color": "#555"}, size="sm"),
            ]
        ),
        dmc.Space(h=30),
        # GitHub Link Card
        dmc.Card(
            children=[
                dmc.Group(
                    [
                        dmc.Text("🔗 Project Repository", size="sm"),
                        dmc.Anchor(
                            "View on GitHub",
                            href="https://github.com/andergod/OrderBookSimulator.git",
                            target="_blank",
                            variant="gradient",
                            gradient={"from": "indigo", "to": "cyan"},
                        ),
                    ],
                ),
            ],
            withBorder=True,
            shadow="sm",
            radius="md",
            p="md",
        ),
        dmc.Space(h=30),
        # Scoping the ideas and arquitecture
        dmc.Stack(
            [
                dmc.Title("Order Book matching ideas", order=2),
                dmc.Stack(
                    [
                        dmc.Text(
                            """ The project is inspired by the architecture used by modern exchanges to match
                                trading orders. Handling thousands or even millions of orders per day requires
                                an extremely time‑sensitive and deterministic infrastructure. Our first step was
                                to study the standard exchange design patterns and map them into a clean,
                                practical architecture.

                                An order book must support ultra‑fast order insertion, matching, and fill routing. 
                                According to the literature, the most efficient approach is to split the book into 
                                two independent structures: bidBook and askBook. Each side maintains its own set of
                                orders and is implemented as a pre‑allocated array to guarantee predictable memory 
                                access, cache locality and constant‑time operations.

                                The index of each array corresponds to a specific price point, so all prices must be
                                converted into indexes. This is done using the tick size as a reference. For example, 
                                if index 0 corresponds to a price of 120 for a given future, then index 1 corresponds 
                                to 120 + tick, index 2 to 120 + 2·tick, and so on.

                                We also maintain `best_bid` and `best_ask`, which are the key determinants of
                                whether an incoming order matches immediately or rests in the book. These
                                elements form the essential backbone of any high‑performance order book.""",
                        ),
                        dcc.Markdown(
                            """
                                     ```cpp
                                    struct Order {
                                        int id;
                                        double price;
                                        int qty;
                                    };

                                    class OrderBook {
                                    public:
                                        static constexpr std::size_t MAX_ORDERS = 1024;

                                        // Pre‑allocated arrays for deterministic performance
                                        std::array<Order, MAX_ORDERS> bidBook{};
                                        std::array<Order, MAX_ORDERS> askBook{};

                                        // Track best prices
                                        double best_bid = 0.0;
                                        double best_ask = MAX_ORDERS;

                                        // Insert a buy order
                                        void addBid(const Order& o) {
                                            bidBook[o.id] = o;
                                            if (o.price > best_bid)
                                                best_bid = o.price;
                                        }

                                        // Insert a sell order
                                        void addAsk(const Order& o) {
                                            askBook[o.id] = o;
                                            if (o.price < best_ask)
                                                best_ask = o.price;
                                        }

                                        // Check if an incoming order crosses the spread
                                        bool crossesSpread(const Order& o, bool isBuy) {
                                            return isBuy ? (o.price >= best_ask)
                                                        : (o.price <= best_bid);
                                        }
                                    };
                                    ```
                                                                        """
                        ),
                    ],
                ),
            ]
        ),
        dmc.Space(h=40),
        dmc.Stack(
            [
                dmc.Title(
                    """ We'll introduce 2 types of order books: Deque order books and linked list books""",
                    order=2,
                ),
                dmc.Title("Deque Order Book", order=2),
                dmc.Text(
                    """Deque orderbooks work such that each entry in an array is associated to a price level and this price level, is 
                     defined through a deque. The deque will allow us for an efficient matching meachnism as we could pop from the front 
                     at O(1) constant time, while at the same time allowing us to push new orders at this simple time complexity. The main
                     strenght of the deque is also its weakness, given the standard method usages allows for easy matches and adding orders
                     on queue. 
                     
                     However, in this setup we're introduce to one of my first big struggles. How do we cancel orders efficiently? The answer
                     seemed quite simple, we reproduce a unordered_map with id's as dictionaries and then we hold some info related to the
                     order like side, price and a pointer to its position on its deque. Then, theorically, we could go and delete the element 
                     relatively simple in O(1) by getting the ID numbers. However, deque's pointers are not stable through middle element
                     elimination, meaning all the pointers that are trapped in the middle of this elimination are corrupt and our initial
                     unoreded map becomes obsolete. Therefore, we found a middle solution, although not efficient, we introduce a share_ptr, 
                     which allow to keep the order on scope even though they get eliminated, and the pointers are still on scope 
                     when deleting. However, this comes as a cost, the orders no longer live on the array itself (cache), no, as a share_ptr they 
                     live on the stack reducing the potential performance of our output. 
                     """
                ),
                dcc.Markdown(
                    """
                    ```cpp
                    class dequeOrderBook : public orderBook<dequeOrderBook>
                    {
                    private:
                        friend class orderBook<dequeOrderBook>;
                        std::vector<int32_t> pushOrder(std::shared_ptr<order> cleanRec, std::int32_t priceIdx, Side side);
                        std::vector<int32_t> matchOrder(std::shared_ptr<order> cleanRec, std::int32_t priceIdx, Side side, std::int32_t &bestPxIdx);
                        std::vector<int32_t> matchAtPriceLevel(std::deque<std::shared_ptr<order>> &level, std::shared_ptr<order> &cleanRec);
                        std::unordered_map<std::int32_t, OrderLocation> lookUpMap;
                        void iterativePrint(std::deque<std::shared_ptr<order>> &ordersAtPrice);
                        std::array<std::deque<std::shared_ptr<order>>, MAXTICKS> bidBook;
                        std::array<std::deque<std::shared_ptr<order>>, MAXTICKS> askBook;
                        std::int32_t bestBidIdx = -1;
                        std::int32_t bestAskIdx = MAXTICKS;
                        void CheckLookUpMap(std::unordered_map<std::int32_t, OrderLocation> &lookUpMap);

                    public:
                        // orderBook definition
                        dequeOrderBook();
                        // method for adding a limit order into the order book and match it if necessary
                        std::vector<int32_t> addLimitOrderImpl(orderReceived received);
                        void updateNextWorstPxIdxImpl(const Side side);
                        std::vector<int32_t> modifyOrderImpl(amendOrder modOrder);
                        void cancelOrderImpl(amendOrder modOrder);
                        // show the contect of the book
                        void showBookImpl();
                        void showLookUpMapImpl();
                        // vector that holds the trades
                        std::vector<tradeRecord> trades;
                    };
                    """
                ),
                dmc.Space(h=30),
                dmc.Title("Linked List Order Book", order=2),
                dmc.Text(
                    """
                    To address the limitations of our current setup, we switch to a linked‑list–style structure. A linked list gives us constant‑time 
                    operations at both the front and back, which is ideal for managing order queues. However, a traditional linked list still suffers 
                    from the same major drawback as before: poor cache locality. In fact, its locality is even worse than that of a deque because each
                    node is typically allocated separately and scattered across memory.

                    To mitigate this, we keep the same idea of storing a pointer to the node we want to cancel, allowing direct access without searching. 
                    But to improve cache locality, we introduce a pool allocator. Instead of allocating each node independently on the heap, we reserve a 
                    continuous block of memory—a pre‑allocated array—and carve it into nodes using pointers. The linked‑list nodes then live inside this 
                    compact region.

                    This approach preserves the flexibility of a linked list while significantly improving spatial locality and reducing allocation 
                    overhead, giving us predictable performance without the drawbacks of a deque’s block‑segmented design.
                    """
                ),
                dcc.Markdown(
                    """
                    ```cpp
                    class intrusiveOrderBook : public orderBook<intrusiveOrderBook>
                    {
                    private:
                        friend class orderBook<intrusiveOrderBook>;
                        OrderPool orderPool;
                        std::vector<int32_t> pushOrder(OrderIntrusive *cleanRec, std::int32_t priceIdx, Side side);
                        std::vector<int32_t> matchOrder(OrderIntrusive *cleanRec, std::int32_t priceIdx, Side side, std::int32_t &bestPxIdx);
                        void iterativePrint(OrderList &ordersAtPrice);
                        void updateNextWorstPxIdxImpl(const Side side);
                        std::vector<int32_t> matchAtPriceLevel(OrderList &level, OrderIntrusive *cleanRec);
                        std::unordered_map<std::int32_t, OrderLocationIntrusive> lookUpMap;
                        std::array<OrderList, MAXTICKS> bidBook;
                        std::array<OrderList, MAXTICKS> askBook;
                        std::int32_t bestBidIdx = -1;
                        std::int32_t bestAskIdx = MAXTICKS;
                        void CheckLookUpMap(std::unordered_map<std::int32_t, OrderLocationIntrusive> &lookUpMap);

                    public:
                        // orderBook definition
                        intrusiveOrderBook() : orderPool(1000 * MAXTICKS) {};
                        // method for adding a limit order into the order book and match it if necessary
                        std::vector<int32_t> addLimitOrderImpl(orderReceived received);
                        std::vector<int32_t> modifyOrderImpl(amendOrder modOrder);
                        void cancelOrderImpl(amendOrder modOrder);
                        // show the contect of the book
                        void showBookImpl();
                        void showLookUpMapImpl();
                        // vector that holds the trades
                        std::vector<tradeRecord> trades;
                    };
                    """
                ),
            ]
        ),
    ],
    size="xl",
    style={"padding": "2rem"},
)
