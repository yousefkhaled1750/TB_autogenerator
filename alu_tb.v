`timescale 1us/1ns
module ALU_tb ();
	parameter	WIDTH_tb = 8;
	parameter	MUL_WIDTH_tb = 12;
	reg 	[WIDTH_tb - 1 : 0]	a_tb;
	reg 	[WIDTH_tb - 1 : 0]	b_tb;
	reg 	[3:0]				opsel_tb;
	reg 						in_tb;
	reg 						cond1_tb;
	reg 						cond2_tb;
	wire 	[MUL_WIDTH_tb - 1 : 0]	result_tb;
	wire 						out_tb;
	reg		[12:0]				initial_state;


ALU #(
.WIDTH(WIDTH_tb),
.MUL_WIDTH(MUL_WIDTH_tb)
) DUT (
	.a(a_tb),
	.b(b_tb),
	.opsel(opsel_tb),
	.in(in_tb),
	.cond1(cond1_tb),
	.cond2(cond2_tb),
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
	cond1_tb = 1'b0 ;
	cond2_tb = 1'b0 ;


//parsing the case statements
	opsel_tb = 4'd0; a_tb = 103; b_tb = 84;
#1
	if(result_tb == (a_tb + b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd1; a_tb = 63; b_tb = 70;
#1
	if(result_tb == (a_tb - b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd2; a_tb = 39; b_tb = 31;
#1
	if(result_tb == (a_tb * b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd3; a_tb = 62; b_tb = 109;
#1
	if(result_tb == (a_tb >>> b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd4; a_tb = 27; b_tb = 109;
#1
	if(result_tb == (a_tb <<< b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd5; a_tb = 102; b_tb = 119;
#1
	if(result_tb == (a_tb / b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd6; a_tb = 90;
#1
	if(result_tb == (~a_tb ))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd7; a_tb = 91; b_tb = 107;
#1
	if(result_tb == (a_tb & b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd8; a_tb = 9; b_tb = 6;
#1
	if(result_tb == (a_tb | b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd9; a_tb = 8; b_tb = 71;
#1
	if(result_tb == (a_tb ^ b_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	opsel_tb = 4'd10; 
#1
	if(result_tb == ('d1))
		$display("Successful Test!");
	else
		$display("Failed Test!");


//parsing the if statements
	cond1_tb = 1; 	in_tb = 0;
#1
	if(out_tb == (in_tb ))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	cond1_tb = 0; 
	cond2_tb = 1; 	in_tb = 1;
#1
	if(out_tb == (~in_tb ))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	cond2_tb = 0; 
#1
	if(out_tb == (0))
		$display("Successful Test!");
	else
		$display("Failed Test!");

	repeat(30) begin
	#1
		a_tb = $random % 256;
		b_tb = $random % 256;
		opsel_tb = $random % 16;
		in_tb = $random % 2;
		cond1_tb = $random % 2;
		cond2_tb = $random % 2;
	end

#100 $stop;

end



initial begin 
	$monitor($time, ": a = %d; b = %d; opsel = %d; in = %d; cond1 = %d; cond2 = %d; result = %d; out = %d; ",a_tb ,b_tb ,opsel_tb ,in_tb ,cond1_tb ,cond2_tb ,result_tb ,out_tb );
end



endmodule