`timescale 1us/1ns
module ALU_tb ();
	parameter	WIDTH_tb = 8;
	parameter	MUL_WIDTH_tb = 16;
	reg 	[WIDTH_tb - 1 : 0]	a_tb;
	reg 	[WIDTH_tb - 1 : 0]	b_tb;
	reg 	[2:0]				opsel_tb;
	wire 	[MUL_WIDTH_tb - 1 : 0]	result_tb;


ALU #(
.WIDTH(WIDTH_tb),
.MUL_WIDTH(MUL_WIDTH_tb)
) DUT (
	.a(a_tb),
	.b(b_tb),
	.opsel(opsel_tb),
	.result(result_tb)
	);

initial begin 
	$dumpfile("ALU.vcd");
	$dumpvars;

	a_tb = 'b0 ;
	b_tb = 'b0 ;
	opsel_tb = 3'b0 ;


	repeat(30) begin
		a_tb = $random % 256;
		b_tb = $random % 256;
		opsel_tb = $random % 8;
	end

#100 $stop;

end



initial begin 
	$monitor($time, ": a = %d; b = %d; opsel = %d; result = %d; ",a_tb ,b_tb ,opsel_tb ,result_tb );
end



endmodule