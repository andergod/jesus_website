import dash
from dash import html, dcc, Input, Output, callback
import dash_mantine_components as dmc

import dash
from dash import html, dcc
import dash_mantine_components as dmc

dash.register_page(__name__, path="/projects/bar-generation", name="Bar Generation")

layout = dmc.Container(
    size="xl",
    style={"padding": "2rem"},
    children=[
        dmc.Space(h=30),
        # Project Header
        dmc.Stack(
            [
                dmc.Title("Bar generation in C++", order=1),
                dmc.Group(
                    [
                        dmc.Badge("C++", size="lg", variant="dot"),
                        dmc.Badge("Networking", size="lg", variant="dot"),
                        dmc.Badge("Bar Generation", size="lg", variant="dot"),
                        dmc.Badge("Tick data", size="lg", variant="dot"),
                    ]
                ),
                dmc.Text("Published: Mar 30, 2026", style={"color": "#555"}, size="sm"),
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
                # Networking setup
            ]
        ),
        dmc.Space(h=30),
        dmc.Stack(
            children=[
                dmc.Title("Set up", order=2),
                dmc.Text(
                    """
                    Probably this has been one of the hardest setup I've done. The beast::boost library lives within 
                    the boost library and there are several packages manager out there that may work depending of your
                    situation. I've heard that all of them have their discomforts, so choose your tool. I've decied to
                    use vpckg in the manifest mode. Additionally, most of this library is header-only increasing massively
                    your compiling times. So, i don't recommend deleting your build once you have it. 
                    """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Space(h=30),
                dmc.Title("Networking usage", order=2),
                dmc.Text(
                    """
                    The advantage of using C++ with Boost.Beast is the granular control it offers over the networking stack. 
                    The code below demonstrates the explicit handling of each layer: first, we perform DNS resolution to 
                    translate the hostname into an IP address. Next, we establish the raw TCP connection (Layer 4). 
                    Once connected, we initiate the TLS/SSL handshake (Layer 6) to secure the channel, ensuring we set the 
                    SNI (Server Name Indication) correctly. Finally, we perform the WebSocket handshake (Layer 7) to upgrade 
                    the HTTP protocol to a persistent, full-duplex WebSocket connection.
                    """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dcc.Markdown(
                    """
                    ```cpp
                    void WebsocketClient::connect()
                    {
                    load_root_certificates(ctx);

                    auto results = resolver.resolve(host, port);
                    net::connect(beast::get_lowest_layer(ws), results);

                    if (!SSL_set_tlsext_host_name(
                            ws.next_layer().native_handle(), host.c_str())) {
                        throw beast::system_error(
                        static_cast<int>(::ERR_get_error()), net::error::get_ssl_category());
                    }

                    ws.next_layer().handshake(ssl::stream_base::client);
                    ws.handshake(host, target);
                    }
                    """
                ),
                dmc.Space(h=30),
                dmc.Text(
                    """
                    Once the WebSocket connection is established, we need a way to receive messages. The `readMessage` function 
                    handles this by first clearing the dynamic buffer to ensure no stale data is processed. It then performs a 
                    blocking read on the WebSocket stream, waiting for a complete message from the server. Once received, the raw 
                    message data stored in the buffer is converted into a `std::string` for easier parsing and subsequent processing 
                    by the bar generation logic.
                    """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dcc.Markdown(
                    """
                    ```cpp
                    std::string WebsocketClient::readMessage()
                    {
                    buffer.consume(buffer.size());
                    ws.read(buffer);
                    return beast::buffers_to_string(buffer.data());
                    }
                    """
                ),
                dmc.Space(h=30),
                dmc.Title("Order Book", order=2),
                dmc.Text(
                    """
                    This is probably the most complex object in our bar‑generation system, and also the one I’m least satisfied with. Even 
                    so, it’s a solid implementation that handles multiple figures simultaneously. I chose not to keep adding more methods 
                    and will instead introduce additional abstractions if needed. The order book will track the full state of the market, 
                    and its initial structure closely follows the approach used in our previous Order Book implementation.
                    """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dcc.Markdown(
                    """
                ## Core Responsibilities

                This component performs three main functions:

                1. **Maintain the L2 orderbook** by applying incoming incremental updates.
                2. **Continuously update the Top‑of‑Book (ToB)** to reflect the current best bid and ask.
                3. **Generate bars in O(1)** time as each new update arrives.
                    """
                ),
                dmc.Text(
                    """
                    Given the first method is a copy of our last note, I'll focus on the second implementation and so on.
                    The importat bits to remember is that this will hold and update the bestBid (maxBidIdx) and bestAsk (minAskIdx)
                    as new orders come in. Meaning, we can take advantage of those to rapidly update our ToB and reupdate our ToB after
                    each new event. We'll use a struct to save those values and constantly update them with every need event. 
                    """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dcc.Markdown(
                    """
                    ```cpp
                    
                    struct topOfBook {
                    double                                                  price_bid;
                    double                                                  price_ask;
                    double                                                  bid_quantity;
                    double                                                  ask_quantity;
                    time_point<system_clock, duration<uint64_t, std::nano>> time;
                    };  
                    
                    void updateToB(time_point<system_clock, duration<uint64_t, std::nano>> time)
                    {
                        if (maxBidIdx >= 0) {
                        latestToB.price_bid    = MINPRICE + maxBidIdx * TICKSIZE;
                        latestToB.bid_quantity = bidBook[maxBidIdx];
                        }
                        else {
                        latestToB.price_bid    = 0.0;
                        latestToB.bid_quantity = 0.0;
                        }

                        if (minAskIdx < static_cast<std::int32_t>(MAXTICKS)) {
                        latestToB.price_ask    = MINPRICE + minAskIdx * TICKSIZE;
                        latestToB.ask_quantity = askBook[minAskIdx];
                        }
                        else {
                        latestToB.price_ask    = 0.0;
                        latestToB.ask_quantity = 0.0;
                        }
                        latestToB.time = time;
                    };
                    """
                ),
                dmc.Space(h=10),
                dmc.Text(
                    """
                         Then we move on to the core of bar creation. We set up a struct that holds the bar details, and we continuously update these values as new data arrives. This allows us to consolidate statistics when the bar’s lifetime ends (e.g., computing averages or medians of any ToB metric). The relevant code is shown below: """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dcc.Markdown(
                    """
                             ```cpp

                                struct curr_state {
                                double   curr_start_bid;
                                double   curr_end_bid;
                                double   curr_high_bid;
                                double   curr_low_bid;
                                double   curr_sum_bid;
                                double   curr_sum_bid_size;
                                double   curr_start_ask;
                                double   curr_end_ask;
                                double   curr_high_ask;
                                double   curr_low_ask;
                                double   curr_sum_ask;
                                double   curr_sum_ask_size;
                                uint64_t cum_time;
                                uint64_t curr_bid_update_count;
                                uint64_t curr_ask_update_count;
                                };
                                
                               void barUpdate()
                                {
                                    if (latestToB.price_bid > 0) {
                                    if (current_state.curr_start_bid == 0.0) { // First bid update for this
                                        current_state.curr_start_bid = latestToB.price_bid;
                                    }
                                    if (latestToB.price_bid < current_state.curr_low_bid)
                                        current_state.curr_low_bid = latestToB.price_bid;
                                    if (latestToB.price_bid > current_state.curr_high_bid)
                                        current_state.curr_high_bid = latestToB.price_bid;
                                    current_state.curr_end_bid = latestToB.price_bid;
                                    avgBidPriceHeap.push(latestToB.price_bid);
                                    avgBidSizeHeap.push(latestToB.bid_quantity);
                                    current_state.curr_bid_update_count++;
                                    }

                                    if (latestToB.price_ask > 0) {
                                    if (current_state.curr_start_ask == 0.0) { // First ask update for this
                                        current_state.curr_start_ask = latestToB.price_ask;
                                    }
                                    if (latestToB.price_ask < current_state.curr_low_ask)
                                        current_state.curr_low_ask = latestToB.price_ask;
                                    if (latestToB.price_ask > current_state.curr_high_ask)
                                        current_state.curr_high_ask = latestToB.price_ask;
                                    current_state.curr_end_ask = latestToB.price_ask;
                                    avgAskPriceHeap.push(latestToB.price_ask);
                                    avgAskSizeHeap.push(latestToB.ask_quantity);
                                    current_state.curr_ask_update_count++;
                                    }
                                };
                            ```
                             """
                ),
                dmc.Text(
                    """
                        I use a heap-based algorithm to compute the median of all elements in the stream. Each new value is inserted in O(log n) time, and once the bar closes we can retrieve the median in O(1) time. """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Text(
                    """ Finally, we can complete the bar. Most statistics simply take the latest update, but some require aggregation. For example, a quote‑weighted average would be computed as the total sum of bids divided by the total number of updates. In this case, I use the heap structure to keep the median readily available.
                    """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dcc.Markdown(
                    """ 
                    ```cpp
                        struct bar {
                            double                                                  startBid;
                            double                                                  endBid;
                            double                                                  highBid;
                            double                                                  lowBid;
                            double                                                  avgBid;
                            double                                                  avgBidSize;
                            double                                                  startAsk;
                            double                                                  endAsk;
                            double                                                  highAsk;
                            double                                                  lowAsk;
                            double                                                  avgAsk;
                            double                                                  avgAskSize;
                            std::int32_t                                            bid_quote_count;
                            std::int32_t                                            ask_quote_count;
                            std::int32_t                                            tradeQuantity;
                            time_point<system_clock, duration<uint64_t, std::nano>> time;
                        };
                            
                        bar createBar()
                            {
                                bar newBar{}; // zero initialize

                                if (
                                current_state.curr_bid_update_count > 0
                                || current_state.curr_ask_update_count > 0) {
                                newBar.time = now_timepoint();
                                }

                                if (current_state.curr_bid_update_count > 0) {
                                newBar.startBid        = current_state.curr_start_bid;
                                newBar.endBid          = current_state.curr_end_bid;
                                newBar.highBid         = current_state.curr_high_bid;
                                newBar.lowBid          = current_state.curr_low_bid;
                                newBar.avgBid          = avgBidPriceHeap.getMedian();
                                newBar.avgBidSize      = avgBidSizeHeap.getMedian();
                                newBar.ask_quote_count = current_state.curr_ask_update_count;
                                }

                                if (current_state.curr_ask_update_count > 0) {
                                newBar.startAsk        = current_state.curr_start_ask;
                                newBar.endAsk          = current_state.curr_end_ask;
                                newBar.highAsk         = current_state.curr_high_ask;
                                newBar.lowAsk          = current_state.curr_low_ask;
                                newBar.avgAsk          = avgAskPriceHeap.getMedian();
                                newBar.avgAskSize      = avgAskSizeHeap.getMedian();
                                newBar.bid_quote_count = current_state.curr_bid_update_count;
                                }
                                return newBar;
                        }
                             """
                ),
                dmc.Title("Parquet saving", order=2),
                dmc.Text(
                    """
                If you’ve reached this stage, saving the element as a Parquet file is not difficult from a CMake/vcpkg perspective, and the code itself is even simpler. It’s essentially a matter of taking the fields from our bar struct and passing them into a Parquet writer. My approach is a bit verbose, as I didn’t want to over‑engineer or introduce a new abstraction layer around Parquet generation for this struct. Instead, I follow a straightforward method, and I’ll show a small example below:
                         """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dmc.Text(
                    """
                I would describe it as essentially a two‑step process: first, we create the RecordBatch object with the schema defined inside the initial convertToArrow function. Then, we write the data out in Parquet format using Snappy compression, optionally specifying a row‑group size if we want to split the output into chunks for partitioned datasets.
                         """,
                    style={"textAlign": "justify", "marginBottom": 10},
                ),
                dcc.Markdown(
                    """
                    ```cpp
                    inline arrow::Result<std::shared_ptr<arrow::RecordBatch>> convertToArrow(const std::vector<bar>& bars)
                    {
                    arrow::TimestampBuilder time_builder(
                        arrow::timestamp(arrow::TimeUnit::NANO), arrow::default_memory_pool());
                    arrow::DoubleBuilder start_bid_builder;
                    arrow::DoubleBuilder end_bid_builder;

                    for (const auto& b : bars) {
                        ARROW_RETURN_NOT_OK(time_builder.Append(b.time.time_since_epoch().count()));
                        ARROW_RETURN_NOT_OK(start_bid_builder.Append(b.startBid));
                        ARROW_RETURN_NOT_OK(end_bid_builder.Append(b.endBid));
                    }

                    std::shared_ptr<arrow::Array> time_col, start_bid, end_bid;

                    ARROW_RETURN_NOT_OK(time_builder.Finish(&time_col));
                    ARROW_RETURN_NOT_OK(start_bid_builder.Finish(&start_bid));
                    ARROW_RETURN_NOT_OK(end_bid_builder.Finish(&end_bid));

                    auto schema = arrow::schema({
                        arrow::field("time", arrow::timestamp(arrow::TimeUnit::NANO)),
                        arrow::field("startBid", arrow::float64()),
                        arrow::field("endBid", arrow::float64()),
                    });
                    
                    return arrow::RecordBatch::Make(
                    schema,
                    bars.size(),
                    {
                    time_col, start_bid, end_bid,
                    });
                    
                    void saveToParquet(const std::shared_ptr<arrow::RecordBatch>& batch)
                    {
                    // Convert RecordBatch → Table
                    auto table_result = arrow::Table::FromRecordBatches({batch});
                    PARQUET_THROW_NOT_OK(table_result.status());
                    std::shared_ptr<arrow::Table> table = table_result.ValueOrDie();

                    // Open output file
                    std::shared_ptr<arrow::io::FileOutputStream> outfile;
                    PARQUET_ASSIGN_OR_THROW(
                        outfile,
                        arrow::io::FileOutputStream::Open("src/barGeneration/bars.parquet"));

                    // Writer properties
                    parquet::WriterProperties::Builder builder;
                    builder.compression(parquet::Compression::SNAPPY);

                    // Write table
                    PARQUET_THROW_NOT_OK(
                        parquet::arrow::WriteTable(
                        *table,
                        arrow::default_memory_pool(),
                        outfile,
                        5'000'000, // ~5M rows ≈ 256MB for 48-byte rows
                        builder.build()));
                    }
                    """
                ),
            ]
        ),
    ],
)
