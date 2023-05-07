`timescale 1us/1ns
module ALU_tb ();
	parameter	WIDTH_tb = 8;
	parameter	MUL_WIDTH_tb = 12;
	reg 	[WIDTH_tb - 1 : 0]	a_tb;
	reg 	[WIDTH_tb - 1 : 0]	b_tb;
	reg 	[3:0]				opsel_tb;
	reg 						in_tb;
	wire 	[MUL_WIDTH_tb - 1 : 0]	result_tb;
	wire 						out_tb;


ALU #(
.WIDTH(WIDTH_tb),
.MUL_WIDTH(MUL_WIDTH_tb)
) DUT (
	.a(a_tb),
	.b(b_tb),
	.opsel(opsel_tb),
	.in(in_tb),
	.result(result_tb),
	.out(out_tb)
	);

initial begin 
	$dumpfile("ALU.vcd");
	$dumpvars;

	a_tb = 'b0 ;
	b_tb = 'b0 ;
	opsel_tb = 4'b0 ;
	in_tb = 1'b0 ;


	opsel_tb = 4'd0; a_tb = 118; b_tb = 28;
#1
	if(result_tb == (a_tb + b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd1; a_tb = 35; b_tb = 90;
#1
	if(result_tb == (a_tb - b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd2; a_tb = 47; b_tb = 79;
#1
	if(result_tb == (a_tb * b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd3; a_tb = 99; b_tb = 121;
#1
	if(result_tb == (a_tb >>> b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd4; a_tb = 99; b_tb = 90;
#1
	if(result_tb == (a_tb <<< b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd5; a_tb = 98; b_tb = 42;
#1
	if(result_tb == (a_tb / b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd6; a_tb = 33;
#1
	if(result_tb == (~a_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd7; a_tb = 0; b_tb = 77;
#1
	if(result_tb == (a_tb & b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd8; a_tb = 69; b_tb = 21;
#1
	if(result_tb == (a_tb | b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd9; a_tb = 107; b_tb = 80;
#1
	if(result_tb == (a_tb ^ b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd10; a_tb = 127;#1
	if(result_tb == (a_tb + 'd1))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	repeat(30) begin
	#1
		a_tb = $random % 256;
		b_tb = $random % 256;
		opsel_tb = $random % 16;
		in_tb = $random % 2;
	end

#100 $stop;

end



initial begin 
	$monitor($time, ": a = %d; b = %d; opsel = %d; in = %d; result = %d; out = %d; ",a_tb ,b_tb ,opsel_tb ,in_tb ,result_tb ,out_tb );
end



endmodule