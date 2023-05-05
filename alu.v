module ALU #(
    parameter WIDTH = 8,
    parameter MUL_WIDTH = 16
) (
    input   wire [WIDTH-1:0] a,
    input   wire [WIDTH-1:0] b,
    input   wire [2 : 0]         opsel,
    output  reg  [MUL_WIDTH-1:0] result
);

always @(*) begin
    case (opsel)
        3'd0:   result = a + b;
        3'd1:   result = a - b;
        3'd2:   result = a * b;
        3'd3:   result = a >>> b;
        3'd4:   result = a <<< b;
        3'd5:   result = a + 'd1;
        default: result = a + b;
    endcase
end
    
endmodule