module file #(
    parameter WIDTH = 8,
    parameter signed [7:0] par = 64,
    parameter MUL_WIDTH = WIDTH*2,
)
(
    input   wire    clk,rst,
    input   wire    [7:0] data_in,
    input   wire    a,
    input   wire    b,
    output  reg     [7:0] data_out,
    output  wire    out
);

localparam local = 'd5 ;
wire [7:0] byte;
wire ayhaga;
reg [7:0] register;
reg x;

assign out = a == b;
assign ayhaga = x ? a : b;
assign m = ~|r;

always @(posedge clk, negedge rst) begin
    if (!rst) begin
        data_out <= 'd0;
    end else begin
        data_out <= data_in;
    end
end

always @(*) begin
    x = data_in[0];
end

always @(rst, clk, data_in) begin
    m = data_in[1];
end

endmodule