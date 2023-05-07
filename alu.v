module ALU #(
    parameter WIDTH = 8,
    parameter MUL_WIDTH = 16
) (
    input   wire [WIDTH-1:0] a,
    input   wire [WIDTH-1:0] b,
    input   wire [3 : 0]         opsel,
    output  reg  [MUL_WIDTH-1:0] result,
    input   wire                 in,
    output  reg                  out
);


always @(*) begin
    case (opsel)
        4'd0:   result = a + b;
        4'd1:   result = a - b;
        4'd2:   result = a * b;
        4'd3:   result = a >>> b;
        4'd4:   result = a <<< b;
        4'd5:   result = a / b;
        4'd6:   result = ~a;
        4'd7:   result = a & b;
        4'd8:   result = a | b;
        4'd9:   result = a ^ b;
        4'd10:  result = a + 'd1;
        default: result = a + b;
    endcase
end
    
endmodule