module mix #(
      parameter WIDTH = 8
) 
(
  input     wire          clk,
  input     wire          rst,
  input     wire    [7:0] data_in,
  output    reg     [7:0] data_out,
  input     wire    [7:0] comb_in,
  input     wire    [7:0] comb_add,
  output    wire    [7:0] comb_out,
  input     wire    [7:0] a,
  output    reg     [7:0] out,
  input     wire          sel,
  input     wire          b,
  output    wire          c
);

assign  comb_out = comb_in + comb_add;
assign  c = sel ? b : 0;

  always @(posedge clk, negedge rst) begin
    if (~rst)   data_out <= 0;
    else        data_out <= data_in;
  end

  always @(*) begin
    out = a;
  end

endmodule
