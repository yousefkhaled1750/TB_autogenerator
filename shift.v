module shift #(
    parameter  WIDTH = 8
) (
    input   wire                clk,
    input   wire                rst,
    input   wire                shift_enable,
    input   wire                in_enable,
    input   wire    [WIDTH-1:0] in,
    output  reg     [WIDTH-1:0] out
);

always @(posedge clk, negedge rst) begin
    if (~rst)                out <= 'd0;
    else if (in_enable)     out <= in;            
    else if (shift_enable)  out <= out >>> 1;
    else                    out <= out;        
end

endmodule