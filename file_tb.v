`timescale 1us/1ns
module file_tb ();
	reg 			clk_tb;
	reg 			rst_tb;
	reg 	[3:0]	data_in_tb;
	reg 			a_tb;
	reg 			b_tb;
	reg 			x_tb;
	wire 	[3:0]	data_out_tb;
	wire 			out_tb;


always #(5.0)  clk_tb = ~clk_tb;


file DUT(
	.clk(clk_tb),
	.rst(rst_tb),
	.data_in(data_in_tb),
	.a(a_tb),
	.b(b_tb),
	.x(x_tb),
	.data_out(data_out_tb),
	.out(out_tb)
	);

initial begin 
	$dumpfile("file.vcd");
	$dumpvars;

	clk_tb = 1'd0;
	rst_tb = 1'd1;
#2.0
	rst_tb = 1'd0;
#5.0
	rst_tb = 1'd1;

	data_in_tb = 4'b0 ;
	a_tb = 1'b0 ;
	b_tb = 1'b0 ;
	x_tb = 1'b0 ;


	repeat(16) @(negedge clk_tb) begin
		data_in_tb = $random % 16;
		a_tb = $random % 2;
		b_tb = $random % 2;
		x_tb = $random % 2;
	end

#100 $stop;

end



initial begin 
	$monitor($time, ": data_in = %d; a = %d; b = %d; x = %d; data_out = %d; out = %d; ",data_in_tb ,a_tb ,b_tb ,x_tb ,data_out_tb ,out_tb );
end



endmodule