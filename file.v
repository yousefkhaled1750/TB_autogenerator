module file #(
    parameter WIDTH = 8,
    parameter signed [7:0] par = 64,
    parameter MUL_WIDTH = WIDTH*2
)
(
    input   wire    clk,
    input   wire    rst,
    input   reg    [WIDTH-1:0] data_in,
    input   wire    a,
    input   wire    b,
    input   wire   [4:0] x,
    output  wire     [WIDTH-1:0] data_out,
    output  wire    out,
    output             pp,
    output      reg        d
);

wire    [7:0]   byte;
wire            ayhaga;
reg     [7:0]   register;
reg             m;

assign out = ~ayhaga;
assign ayhaga = x ? a : b;


always @(posedge clk, negedge rst) begin
    if (a)  data_out <= 'd0;
    else if (!rst)  data_out <= data_in + register;
    end


always @(rst, clk, data_in) begin
    m = data_in[1];
end

always @(*) begin
    case (x)
        'd0:    register = data_in + 'd1;
        'd1:    register = ~data_in; 
        default: register = 'd0;
    endcase
end

always @(*) begin
    case (byte)
        'b00:    register =  a;
        'b01:    register = 'd5;
        'b10:    register = ayhaga;
        'b11:    register = ~data_in; 
        default: register = 'd0;
    endcase
end


endmodule