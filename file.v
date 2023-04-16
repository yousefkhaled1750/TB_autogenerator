module file #(
    parameter WIDTH = 8,
    parameter signed [7:0] par = 64,
    parameter MUL_WIDTH = WIDTH*2,
)
(
    input   wire    clk,rst,
    input   wire    [7:0] data_in,
    output  reg     [7:0] data_out
);

localparam local = 'd5 ;
wire [7:0] byte;
wire ayhaga;
reg [7:0] register;
reg x;

assign ayhaga = data_in[3];

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