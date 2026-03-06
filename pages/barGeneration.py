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
                dmc.Text("Published: Mar 10, 2026", style={"color": "#555"}, size="sm"),
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
                    """
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
                    """
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
                    """
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
            ]
        ),
    ],
)
