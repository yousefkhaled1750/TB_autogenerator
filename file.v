module file #(
    parameter WIDTH = 8,
    parameter signed [7:0] par = 64,
    parameter MUL_WIDTH = WIDTH*2
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
reg m;

assign out = a == b;
assign ayhaga = x ? a : b;


always @(posedge clk, negedge rst) begin
    if (!rst)
        data_out <= 'd0;
    else 
        data_out <= data_in + 5;
    end


always @(*) begin
    x = data_in[0];
end

always @(rst, clk, data_in) begin
    m = data_in[1];
end

always @(*) begin
    case (param)
        'd0:    register = data_in + 'd1;
        'd1:    register = ~data_in; 
        default: register = 'd0;
    endcase
end

always @(*) begin
    case (x)
        'd00:    register = data_in + 'd1;
        'd01:    register = 'd3;
        'd10:    register = 'd5;
        'd11:    register = ~data_in; 
        default: register = 'd0;
    endcase
end


endmodule