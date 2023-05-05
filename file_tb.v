`timescale 1us/1ns
module file_tb ();
	parameter	WIDTH_tb = 8;
	parameter	par_tb = 3;
	parameter	MUL_WIDTH_tb = 16;
	reg 						clk_tb;
	reg 						rst_tb;
	reg 	[WIDTH_tb - 1 : 0]	data_in_tb;
	reg 						a_tb;
	reg 						b_tb;
	reg 	[4:0]				x_tb;
	wire 	[WIDTH_tb - 1 : 0]	data_out_tb;
	wire 						out_tb;
	wire 						d_tb;
	reg 	[WIDTH_tb - 1 : 0]	data_out_exp;
	reg 						out_exp;
	reg 						d_exp;


	reg		[14:0]	test_vect [9:0];
	reg		[31:0]	vecnum, errors;


always #(5.0)  clk_tb = ~clk_tb;


file #(
.WIDTH(WIDTH_tb),
.par(par_tb),
.MUL_WIDTH(MUL_WIDTH_tb)
) DUT (
	.clk(clk_tb),
	.rst(rst_tb),
	.data_in(data_in_tb),
	.a(a_tb),
	.b(b_tb),
	.x(x_tb),
	.data_out(data_out_tb),
	.out(out_tb),
	.d(d_tb)
	);

initial begin 
	$dumpfile("file.vcd");
	$dumpvars;

	$readmemb("ref.txt",test_vect);	vecnum = 32'd0; errors = 32'd0;
	clk_tb = 1'd0;
	rst_tb = 1'd1;
#2.0
	rst_tb = 1'd0;
#5.0
	rst_tb = 1'd1;

	data_in_tb = WIDTH'b0 ;
	a_tb = 1'b0 ;
	b_tb = 1'b0 ;
	x_tb = 5'b0 ;


	repeat(10) @(negedge clk_tb) begin
		{data_in_tb, a_tb, b_tb, x_tb, data_out_exp, out_exp, d_exp} = test_vect[vecnum];
#10
		if(data_out_exp == data_out_tb &&out_exp == out_tb &&d_exp == d_tb)
			$display("Successful Test Case!");
		else
			$display("Failed Test Case!");
		vecnum = vecnum + 1;
	end

	repeat(30) @(negedge clk_tb) begin
		data_in_tb = $random % 256;
		a_tb = $random % 2;
		b_tb = $random % 2;
		x_tb = $random % 32;
	end

#100 $stop;

end



initial begin 
	$monitor($time, ": data_in = %d; a = %d; b = %d; x = %d; data_out = %d; out = %d; d = %d; ",data_in_tb ,a_tb ,b_tb ,x_tb ,data_out_tb ,out_tb ,d_tb );
end



endmodule