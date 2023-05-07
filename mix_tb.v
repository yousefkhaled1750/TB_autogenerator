`timescale 1us/1ns
module mix_tb ();
	parameter	WIDTH_tb = 8;
	reg 						clk_tb;
	reg 						rst_tb;
	reg 	[7:0]				data_in_tb;
	reg 	[7:0]				comb_in_tb;
	reg 	[7:0]				comb_add_tb;
	reg 	[7:0]				a_tb;
	reg 						sel_tb;
	reg 						b_tb;
	wire 	[7:0]				data_out_tb;
	wire 	[7:0]				comb_out_tb;
	wire 	[7:0]				out_tb;
	wire 						c_tb;
	reg		[8:0]				initial_state;


always #(5.0)  clk_tb = ~clk_tb;


mix #(
.WIDTH(WIDTH_tb)
) DUT (
	.clk(clk_tb),
	.rst(rst_tb),
	.data_in(data_in_tb),
	.comb_in(comb_in_tb),
	.comb_add(comb_add_tb),
	.a(a_tb),
	.sel(sel_tb),
	.b(b_tb),
	.data_out(data_out_tb),
	.comb_out(comb_out_tb),
	.out(out_tb),
	.c(c_tb)
	);

initial begin 
	$dumpfile("mix.vcd");
	$dumpvars;

	clk_tb = 1'd0;
	rst_tb = 1'd1;
#2.0
	rst_tb = 1'd0;
#5.0
	rst_tb = 1'd1;

	data_in_tb = 8'b0 ;
	comb_in_tb = 8'b0 ;
	comb_add_tb = 8'b0 ;
	a_tb = 8'b0 ;
	sel_tb = 1'b0 ;
	b_tb = 1'b0 ;


//parsing the case statements


//parsing the if statements
	rst_tb = 0; 
#10
	if(data_out_tb == (0))
		$display("Successful Test!");
	else
		$display("Failed Test!");
	rst_tb = 1; 
#10
	if(data_out_tb == (data_in_tb ))
		$display("Successful Test!");
	else
		$display("Failed Test!");


// parsing the continuous assignments
	comb_in_tb = 6;	comb_add_tb = 34;
#1
	if(comb_out_tb == (comb_in_tb + comb_add_tb))
		$display("Successful Test!");
	else
		$display("Failed Test!");

	sel_tb = 1; 	b_tb = 0;
#1
	if(c_tb == (b_tb ))
		$display("Successful Test!");
	else
		$display("Failed Test!");

// parsing the always assignments
	a_tb = 86;
#1
	if(out_tb == (a_tb ))
		$display("Successful Test!");
	else
		$display("Failed Test!");

	a_tb = 75;
#1
	if(out_tb == (a_tb ))
		$display("Successful Test!");
	else
		$display("Failed Test!");


	repeat(30) @(negedge clk_tb) begin
	#1
		data_in_tb = $random % 256;
		comb_in_tb = $random % 256;
		comb_add_tb = $random % 256;
		a_tb = $random % 256;
		sel_tb = $random % 2;
		b_tb = $random % 2;
	end

#100 $stop;

end



initial begin 
	$monitor($time, ": data_in = %d; comb_in = %d; comb_add = %d; a = %d; sel = %d; b = %d; data_out = %d; comb_out = %d; out = %d; c = %d; ",data_in_tb ,comb_in_tb ,comb_add_tb ,a_tb ,sel_tb ,b_tb ,data_out_tb ,comb_out_tb ,out_tb ,c_tb );
end



endmodule