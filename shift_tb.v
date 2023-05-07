`timescale 1us/1ns
module shift_tb ();
	parameter	WIDTH_tb = 8;
	reg 						clk_tb;
	reg 						rst_tb;
	reg 						shift_enable_tb;
	reg 						in_enable_tb;
	reg 	[WIDTH_tb - 1 : 0]	in_tb;
	wire 	[WIDTH_tb - 1 : 0]	out_tb;
	reg		[8:0]				initial_state;


always #(5.0)  clk_tb = ~clk_tb;


shift #(
.WIDTH(WIDTH_tb)
) DUT (
	.clk(clk_tb),
	.rst(rst_tb),
	.shift_enable(shift_enable_tb),
	.in_enable(in_enable_tb),
	.in(in_tb),
	.out(out_tb)
	);

initial begin 
	$dumpfile("shift.vcd");
	$dumpvars;

	clk_tb = 1'd0;
	rst_tb = 1'd1;
#2.0
	rst_tb = 1'd0;
#5.0
	rst_tb = 1'd1;

	shift_enable_tb = 1'b0 ;
	in_enable_tb = 1'b0 ;
	in_tb = 'b0 ;


//parsing the case statements


//parsing the if statements
	rst_tb = 0; 
#10
	if(out_tb == ('d0))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	rst_tb = 1; 
	in_enable_tb = 1; 	in_tb = 26;
#10
	if(out_tb == (in_tb ))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	in_enable_tb = 0; 
	shift_enable_tb = 1; 	initial_state = out_tb;
#10
	if(out_tb == (initial_state>>> 1))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	shift_enable_tb = 0; 
	initial_state = out_tb;#10
	if(out_tb == (initial_state))
		$display("Successful Test!");
	else
		$display("Failed Test!");

	repeat(30) @(negedge clk_tb) begin
	#1
		shift_enable_tb = $random % 2;
		in_enable_tb = $random % 2;
		in_tb = $random % 256;
	end

#100 $stop;

end



initial begin 
	$monitor($time, ": shift_enable = %d; in_enable = %d; in = %d; out = %d; ",shift_enable_tb ,in_enable_tb ,in_tb ,out_tb );
end



endmodule